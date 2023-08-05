from keras import models
from keras.layers import Input, Dense, LSTM
from keras import layers

from ..model import Model

from ...lib.text_lib import *

from ...lib.general_lib import *

import numpy as np

import random



class Translation_Model(Model):
    def __init__(self, input_shape = None, model_path = None):
        """Initializes a model.
        
        Arguments:
            Model {class} -- A super class of neural network models.
        
        Keyword Arguments:
            input_shape {tuple} -- An input shape of the neural network. (default: {None})
            model_path {str} -- A path of model file. (default: {None})
        """
        if type(input_shape) == type(None):
            Model.__init__(self)
        else:
            Model.__init__(self)
            self.input_shape = input_shape

    def set_input_dictionary(self, input_dictionary):
        self.model.input_dictionary = input_dictionary
        self.model.__class__.input_dictionary = self.model.input_dictionary

    def prepare_train_data(self, input_texts, target_texts, input_characters, target_characters):
        if hasattr(self, 'model') == False:
            encoder_input_size = max([len(txt) for txt in input_texts])
            decoder_input_size = max([len(txt) for txt in target_texts])
            num_of_input_chars = len(input_characters)
            num_of_target_chars = len(target_characters)
            self.encoder_input_data = np.zeros( (len(input_texts), encoder_input_size, num_of_input_chars), dtype='float32' )
            self.decoder_input_data = np.zeros( (len(input_texts), decoder_input_size, num_of_target_chars), dtype='float32' )
            self.decoder_target_data = np.zeros( (len(input_texts), decoder_input_size, num_of_target_chars), dtype='float32' )
            input_char_index = dict( [(char, i) for i, char in enumerate(input_characters)] )
            target_char_index = dict( [(char, i) for i, char in enumerate(target_characters)] )
            self.model, self.encoder_model, self.decoder_model = self.create_model()
            self.set_input_dictionary( reverse_dict(input_char_index) )
            self.set_output_dictionary( reverse_dict(target_char_index) )
        else:
            # train data preparation process after loading a model from file should be implemented
            input_char_index = reverse_dict(self.model.input_dictionary)
            target_char_index = reverse_dict(self.model.output_dictionary)
        for i, (input_text, target_text) in enumerate( zip(input_texts, target_texts) ):
            for t, char in enumerate(input_text):
                self.encoder_input_data[i, t, input_char_index[char]] = 1.
            for t, char in enumerate(target_text):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                self.decoder_input_data[i, t, target_char_index[char]] = 1.
                if t > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start character.
                    self.decoder_target_data[i, t - 1, target_char_index[char]] = 1.
    
    def create_model(self):
        encoder_inputs = Input( shape = ( None, len(self.model.input_dictionary) ) )
        encoder = LSTM(256, return_state = True)
        encoder_outputs, state_h, state_c = encoder(encoder_inputs)
        encoder_states = [state_h, state_c]        
        
        encoder_model = models.Model(encoder_inputs, encoder_states)

        decoder_state_input_h = Input(shape=(256, ))
        decoder_state_input_c = Input(shape=(256, ))
        decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
        
        decoder_inputs = Input( shape = ( None, len(self.model.output_dictionary) ) )
        decoder_lstm = LSTM(256, return_sequences = True, return_state = True)
        decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state = encoder_states)
        decoder_states = [state_h, state_c]
        decoder_dense = Dense(len(self.model.output_dictionary), activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)
        
        decoder_model = models.Model( [[decoder_inputs] + decoder_states_inputs, decoder_outputs] + decoder_states )

        model = models.Model( [encoder_inputs, decoder_inputs], decoder_outputs )

        return model, encoder_model, decoder_model

    def train(self,
            batch_size = None,
            steps_per_epoch = None,
            epochs = 1,
            verbose = 1,
            callbacks = None,
            shuffle = True):
            self.compile_model(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
            self.model.fit([self.encoder_input_data, self.decoder_input_data], self.decoder_target_data,
                batch_size=batch_size,
                steps_per_epoch=steps_per_epoch,
                epochs = epochs,
                verbose = verbose,
                callbacks = callbacks,
                shuffle = shuffle)

    def decode_sequence(self, input_text):
        target_char_index = reverse_dict(self.model.output_dictionary)
        
        states_value = self.encoder_model.predict(input_text)
        target_seq = np.zeros( ( 1, 1, len(self.model.output_dictionary) ) )
        target_seq[0, 0, target_char_index['\t']] = 1.

        stop_condition = False
        decoded_sentence = ''
        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict([target_seq] + states_value)
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_char = self.model.output_dictionary[sampled_token_index]
            decoded_sentence += sampled_char
            if (sampled_char == '\n') or (len(decoded_sentence) > len(self.model.output_dictionary)):
                stop_condition = True
            else:
                target_seq = np.zeros( (1, 1, len(self.model.output_dictionary)) )
                target_seq[0, 0, sampled_token_index] = 1.
                states_value = [h, c]
        return decoded_sentence

    def translate_text(self, input_text):
        decoded_sentence = self.decode_sequence(input_text)
        return decoded_sentence

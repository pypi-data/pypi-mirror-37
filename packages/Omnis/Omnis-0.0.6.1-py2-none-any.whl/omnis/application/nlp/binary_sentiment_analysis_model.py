from keras import models
from keras.layers import Input, Dense
from keras.layers import Embedding, Dropout
from keras.layers import Conv1D
from keras.layers import GlobalMaxPooling1D
from keras.layers import Activation

from keras import layers

from ..model import Model

from ...lib.general_lib import *

import numpy as np

import random

import re

from keras.preprocessing import sequence

import keras



class Binary_Sentiment_Analysis_Model(Model):
    def __init__(self, model_path = None):
        """Initializes a model.
        
        Arguments:
            Model {class} -- A super class of neural network models.
        
        Keyword Arguments:
            model_path {str} -- A path of model file. (default: {None})
        """        
        if type(model_path) != type(None):
            Model.__init__(self, model_path)
        else:
            Model.__init__(self)

    def set_input_dictionary(self, input_dictionary):
        self.model.input_dictionary = input_dictionary
        self.model.__class__.input_dictionary = self.model.input_dictionary

    def init_input_data(self, sentiment_texts):
        x = []
        for i, text in enumerate(sentiment_texts):
            word_list = re.sub("[^\w]", " ",  text.lower()).split() # we will lower all words
            single_element = list()
            for word in word_list:                
                if word in self.model.input_dictionary:
                    single_element.append( self.model.input_dictionary[word] )
            x.append(single_element)
        x = sequence.pad_sequences(x, maxlen = self.input_shape[0])
        return x
    
    def prepare_train_data(self, sentiment_texts, boolean_sentiment_values, skip_top, num_of_words_to_consider, max_num_of_word = 100):
        if hasattr(self, 'input_shape') == False:
            word_freq_dict = dict()
            for text in sentiment_texts:
                word_list = re.sub("[^\w]", " ",  text.lower()).split() # we will lower all words
                for word in word_list:
                    if word in word_freq_dict:
                        word_freq_dict[word] += 1
                    else:
                        word_freq_dict[word] = 1
            sorted_words = sorted(word_freq_dict.items(), key = lambda x:x[1], reverse = True)
            words_to_consider = sorted_words[skip_top : skip_top + num_of_words_to_consider]
            input_dictionary = dict()
            for i, word_tuple in enumerate(words_to_consider):
                input_dictionary[word_tuple[0]] = i
            self.input_shape = ( max_num_of_word, )
            self.model = self.create_model( len(input_dictionary) )
            self.set_input_dictionary(input_dictionary)            
        self.x = self.init_input_data(sentiment_texts)
        self.y = keras.utils.to_categorical(np.asarray(boolean_sentiment_values, dtype=np.bool), num_classes=2)

    def create_model(self, input_dim):
        input_layer = Input(shape = self.input_shape)
        embedding1 = Embedding(input_dim, 128, input_length = self.input_shape[0])(input_layer)
        drop1 = Dropout(0.2)(embedding1)
        conv1 = Conv1D(64, 5, padding='valid', activation='relu', strides=1)(drop1)
        pool1 = GlobalMaxPooling1D()(conv1)
        dense1 = Dense(256)(pool1)
        drop2 = Dropout(0.2)(dense1)
        act1 = Activation('relu')(drop2)
        output_layer = Dense(2, activation = 'sigmoid')(act1)
        return models.Model(inputs=input_layer, outputs=output_layer)

    def train(self,
            batch_size = None,
            steps_per_epoch = None,
            epochs = 1,
            verbose = 1,
            callbacks = None,
            shuffle = True):
            self.compile_model(optimizer = 'nadam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
            self.model.fit(self.x, self.y, batch_size=batch_size, steps_per_epoch=steps_per_epoch, epochs = epochs, verbose = verbose, callbacks = callbacks, shuffle = shuffle)

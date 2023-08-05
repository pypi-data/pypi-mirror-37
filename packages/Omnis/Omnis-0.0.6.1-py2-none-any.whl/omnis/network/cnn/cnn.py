import keras

from keras.preprocessing.image import ImageDataGenerator
import numpy

import os

from keras.models import load_model

import cv2


class CNN:
    """This class is a super class of cnn models.
    """
    def __init__(self, model_path = None):
        """Initialize CNN model with data type specification.

        If you want to load a model you've already trained then just give a path of model file only.
        Otherwise, you should call self.prepare_data() before training your model.
        
        Keyword Arguments:
            model_path {str} -- A path of model file. (default: {None})
        
        Raises:
            e -- Raises error when loading a model is failed.
        """
        self.input_shape = ()
        if type(model_path) == type(None):
            self.model = None
        else:
            try:
                self.model = self.load(model_path)
                if type(self.model) == type(None):
                    print('Nothing loaded')
            except Exception as e:
                print('Model loading failed')
                raise e

    def reshape_image(self, img_array, cv_interpolation = cv2.INTER_LINEAR):
        """This function reshapes a single image.
        
        For now, we only provide a color image cnn model so we only support a GRAY2BGR conversion.
        Check https://github.com/flyyufelix/DenseNet-Keras/issues/18 for default color image format of keras.

        Arguments:
            img_array {ndarray} -- An image array to be reshaped.
        
        Keyword Arguments:
            cv_interpolation {int} -- Opencv interpolation option. (default: {cv2.INTER_LINEAR})
        
        Returns:
            [ndarray] -- Reshaped image array.
        """
        if self.input_shape[2] == img_array.shape[2]:
            resized_array = cv2.resize(img_array, (self.input_shape[0], self.input_shape[1]), interpolation = cv_interpolation)
            return resized_array
        else:
            if img_array.shape[2] == 1 and self.input_shape[2] == 3:
                resized_array = cv2.resize(img_array, (self.input_shape[0], self.input_shape[1]), interpolation = cv_interpolation)
                reshaped_img = cv2.cvtColor(resized_array, cv2.COLOR_GRAY2BGR)
                return reshaped_img
            else:
                # The array is not resize
                return img_array

    def reshape_data(self, data_array, is_image_data):
        """This function change a data array's to model's input shape.
        For now, reshaping is only supported for an array of images.
        
        Arguments:
            data_array {ndarray} -- An array of images.
            is_image_data {bool} -- Check data type.
        
        Returns:
            [ndarray] -- Reshaped data array.
        """
        if is_image_data == False:
            print('it is not recommended to use reshape_data function with non-image data')
        if data_array.shape[1:] != self.input_shape:
            for i in range(data_array.shape[0]):
                if i == 0:
                    x_train_list = [ self.reshape_image(data_array[i]) ]
                else:
                    x_train_list.append( self.reshape_image(data_array[i]) )
            x_train = numpy.array(x_train_list)
            return x_train
        else:
            return data_array

    def prepare_data(self, is_image_data = True, get_image_from = 'directory', data_path = None, data_array = None, label_array = None):
        """This function prepares data for training.
        You MUST prepare data to train your model if you did not initialize your CNN class.
        
        If you want to use CNN model for image classification,
        you should set is_image_data True and get_image_from as 'directory' or 'argument'.
        If you set get_image_from as 'directory',
        you should specify data_path to locate files from a file system
        If you set get_image_from as 'argument',
        you should pass data_array and label_array to prepare your CNN model.

        If you want to use CNN model for other classification problems,
        You MUST pass data_array and label_array.
        
        Keyword Arguments:
            is_image_data {bool} -- Whether your model will be trained with the images or not. (default: {True})
            get_image_from {str} -- Either 'directory' or 'argument'. It is RECOMMENDED to get image from 'directory'. (default: {'directory'})
            data_path {str} -- A path of data directory. Set each label as a subdirectory name. (default: {None})
            data_array {ndarray} -- float32 ndarray ranges from [0, 1]. The same as keras x_train. (default: {None})
            label_array {ndarray} -- ndarray. The same as keras y_train after load_data(). (default: {None})
        """
        self.is_image_data = is_image_data
        self.get_image_from = get_image_from
        self.data_path = data_path
        if self.get_image_from == 'argument':
            if type(data_array) == type(None) or type(label_array) == type(None):
                print('you should prepare arrays to initialize model')
                return
            else:
                print('reshaping data')
                self.x_train = self.reshape_data(data_array, is_image_data)
                self.label_array = label_array
        elif self.get_image_from != 'directory':
            print('value of get_image_from is incorrect')
            return
    
    def create_image_data_generator(self, featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std of the dataset
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            zca_epsilon=1e-06,  # epsilon for ZCA whitening            
            rotation_range=0.,  # randomly rotate images in the range (degrees, 0 to 180)
            width_shift_range=0.,  # randomly shift images horizontally (fraction of total width)
            height_shift_range=0.,  # randomly shift images vertically (fraction of total height)
            brightness_range=None,
            shear_range=0.,  # set range for random shear(Shear angle in counter-clockwise direction in degrees)
            zoom_range=0.,  # set range for random zoom. If a float, `[lower, upper] = [1-zoom_range, 1+zoom_range]`.
            channel_shift_range=0.,  # set range for random channel shifts
            fill_mode='nearest',  # One of {"constant", "nearest", "reflect" or "wrap"}
            cval=0.,  # value used for fill_mode = "constant"
            horizontal_flip=True,  # randomly flip images
            vertical_flip=False,  # randomly flip images
            rescale=None,  # set rescaling factor (applied before any other transformation)
            preprocessing_function=None,  # set function that will be applied on each input
            data_format="channels_last",  # either "channels_first" or "channels_last"
            validation_split=0.0  # fraction of images reserved for validation (strictly between 0 and 1)
        ):
            return ImageDataGenerator(featurewise_center,
                samplewise_center,
                featurewise_std_normalization,
                samplewise_std_normalization,
                zca_whitening,
                zca_epsilon,
                rotation_range,
                width_shift_range,
                height_shift_range,
                brightness_range,
                shear_range,
                zoom_range,
                channel_shift_range,
                fill_mode,
                cval,
                horizontal_flip,
                vertical_flip,
                rescale,
                preprocessing_function,
                data_format,
                validation_split)

    def get_num_of_classes(self, label_array):    
        unique, counts = numpy.unique(label_array, return_counts=True)
        return len(counts)

    def prepare_y_train(self, label_array, num_classes):
        y_train = keras.utils.to_categorical(label_array, num_classes) # convert class vectors to binary class matrices
        return y_train

    def create_model(self, num_classes):
        print('create_model method should be implemented in each model')
        return None

    def train(self,
            image_data_generator = None,
            steps_per_epoch = None,
            epochs = 1,
            verbose = 1,
            callbacks = None,
            shuffle = True,
            use_fit_generator = False
        ):
        """This function trains a model.
        
        Keyword Arguments:
            image_data_generator {ImageDataGenerator} --
                A class which is the same as keras.preprocessing.image.ImageDataGenerator.
                If you know how to use keras, you can pass an argument you want.
                Otherwise, don't worry! Just pass this one.
                (default: {None})
            steps_per_epoch {int or None} -- Total number of steps (batches of samples) before declaring one epoch finished. (default: {None})
            epochs {int} -- Number of epochs to train the model. (default: {1})
            verbose {int} -- Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch. (default: {1})
            callbacks {[type]} --
                List of keras.callbacks.Callback instances.
                If you don't know, then you don't have to use this.
                (default: {None})
            shuffle {bool} -- Has no effect when steps_per_epoch is not None. (default: {True})
            use_fit_generator {bool} --
                Decide whether using keras's fit_generator or not while getting image from an argument.
                Check https://keras.io/models/model/ for usage.
                If you set this one as False, then you can't use image_data_generator.
                If you don't want to know how to use this one, then just pass.
                (default: {False})
        """
        if self.is_image_data == True:
            if type(image_data_generator) == type(None):
                train_datagen = self.create_image_data_generator(rescale = 1./255)
            else:
                train_datagen = image_data_generator

            if self.get_image_from == 'directory':
                train_generator = train_datagen.flow_from_directory(self.data_path, target_size = self.input_shape[:2], class_mode = 'categorical')
                self.model = self.create_model( len(train_generator.class_indices) )
                self.model.compile(optimizer = 'rmsprop', loss = 'categorical_crossentropy', metrics = ['accuracy'])
                self.model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
            elif self.get_image_from == 'argument':
                num_classes = self.get_num_of_classes(self.label_array)
                self.y_train = self.prepare_y_train(self.label_array, num_classes)
                self.model = self.create_model( num_classes )
                self.model.compile(optimizer = 'rmsprop', loss = 'categorical_crossentropy', metrics = ['accuracy'])
                if use_fit_generator == False:
                    self.model.fit(self.x_train, self.y_train, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
                else:
                    train_generator = train_datagen.flow(self.x_train, self.y_train)
                    self.model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
        else:
            num_classes = self.get_num_of_classes(self.label_array)
            self.y_train = self.prepare_y_train(self.label_array, num_classes)
            self.model = self.create_model( num_classes )
            self.model.compile(optimizer = 'rmsprop', loss = 'categorical_crossentropy', metrics = ['accuracy'])
            self.model.fit(self.x_train, self.y_train, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)

    def save(self, save_path = None):
        """This function saves a model as h5 format.
        
        For now, omnis does not automatically understand a type of saved model.
        Therefore, it is recommended to specify your model type on your file name before saving your model.
        In addition, it is recommended to set your model name manually to understand its purpose.
        By default, if user don't pass save_path argument then this function automatically creates a directory and saves a model.

        Keyword Arguments:
            save_path {str} -- Path to save model (default: {None})
        
        Raises:
            e -- Raises error if model is None or save_path is wrong.
        """
        if type(self.model) == type(None):
            print('you should create your model before save it')
        try:
            if type(save_path) == type(None):
                save_dir = os.getcwd() + '/' + str(self)
                if not os.path.isdir(save_dir):
                    os.makedirs(save_dir)                
                model_name = str(self) + '.h5'
                save_path = os.path.join(save_dir, model_name)
            self.model.save(save_path)
        except Exception as e:
            print(e)
            raise e

    def load(self, model_path):
        """This function load a model from a file system.
        
        For now, omnis does not automatically understand a type of saved model.
        Therefore, you should manually initialize a model and load a model with the same type from a file system.

        Arguments:
            model_path {str} -- Path of saved model.
        
        Returns:
           [keras model instance] -- The type of load function is not yet decided. (functional model or sequential model)
        """
        model = load_model(model_path)
        return model

    def predict(self, data):
        """Generates output of predictions for the input samples.
        
        Arguments:
            data {Numpy array} -- The input data like x_test of keras.
        
        Raises:
            e -- Raise exception when prediction failed.
        
        Returns:
            [ndarray] -- Predicted classes(labels) of input data
        """
        try:
            reshaped_data = self.reshape_data(data, self.is_image_data)
            probs = self.model.predict(reshaped_data)
            predicted_classes = probs.argmax(axis=-1)
            return predicted_classes
        except Exception as e:
            # Prediction failed
            raise e

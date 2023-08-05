import keras

from keras.preprocessing.image import ImageDataGenerator
import numpy

import os

import cv2

from ...lib.general_lib import reverse_dict
from ...lib.image_lib import directory_images_to_arrays

from ..model import Model


class CNN(Model):
    """This class is a super class of cnn models.
    """
    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)

    def reshape_image(self, img_array, cv_interpolation = cv2.INTER_LINEAR):
        """Reshapes a single image.
        
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
        """Changes a data array's to model's input shape.
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

    def prepare_train_data(self, is_image_data = True, get_image_from = 'directory', data_path = None, data_array = None, target_array = None):
        """Prepares data for training.
        You MUST prepare data to train your model if you did not initialize your CNN class.
                
        If you want to use CNN model for image classification,
        you should set is_image_data True and get_image_from as 'directory' or 'argument'.
        If you set get_image_from as 'directory',
        you should specify data_path to locate files from a file system.
        If you set get_image_from as 'argument',
        you should pass data_array and target_array to prepare your CNN model.

        If you want to use CNN model for other data classification problems,
        You MUST pass data_array and target_array.
        
        Keyword Arguments:
            is_image_data {bool} -- Whether your model will be trained with the images or not. (default: {True})
            get_image_from {str} -- Either 'directory' or 'argument'. It is RECOMMENDED to get image from 'directory'. (default: {'directory'})
            data_path {str} -- A path of data directory. Set each label as a subdirectory name. (default: {None})
            data_array {ndarray} --
                float32 ndarray.
                If it is not an array of images, all elements of the array should range from [0, 1].
                (default: {None})
            target_array {ndarray} -- ndarray. Appropriate outputs of input data. (default: {None})
        """
        self.is_image_data = is_image_data
        self.get_image_from = get_image_from
        self.data_path = data_path
        if self.get_image_from == 'argument':
            if type(data_array) == type(None) or type(target_array) == type(None):
                print('you should prepare arrays to initialize model')
                return
            else:
                print('reshaping data')
                self.x_train = self.reshape_data(data_array, is_image_data)
                self.target_array = target_array
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

    def create_class_indices(self, unique_classes):
        class_indices = dict()
        for i in range(unique_classes.shape[0]):
            class_indices[unique_classes[i]] = i
        return class_indices

    def create_model(self, num_classes):
        print('create_model method should be implemented in each model')
        return None

    def init_class_dictionary_and_model(self, class_indices, num_classes):
        """Initializes self.class_dictionary and self.model.
        
        Arguments:
            class_indices {dict} -- A reversed dictionary of class_dictionary.
            num_classes {int} -- A number of classes to classify.
        """
        self.set_class_dictionary( reverse_dict(class_indices) )
        self.model = self.create_model( num_classes )
        return

    def prepare_y(self, target_array, class_indices, num_classes):
        """Prepares y for a keras model.(ex. y_train)
        
        Arguments:
            target_array {ndarray} -- ndarray. Appropriate outputs of input data.
            class_indices {dict} --
                A dictionary of classes to targets.
                (A reversed dictionary of self.class_dictionary)
            num_classes {int} -- A number of the entire classes.
        
        Returns:
            [ndarray] -- A binary matrix representation of the input.
        """
        y_list = list()
        for i in range(target_array.shape[0]):
            label_class = class_indices[target_array[i]]
            y_list.append(label_class)
        
        y = keras.utils.to_categorical(numpy.array(y_list), num_classes)
        return y

    def train(self,
            image_data_generator = None,
            batch_size=None,
            steps_per_epoch = None,
            epochs = 1,
            verbose = 1,
            callbacks = None,
            shuffle = True,
            use_fit_generator = False
        ):
        """Trains a model.
        This method automatically checks an existence of self.model.
        If it does not exist automatically, this method will initialize a model with an information of train data.
        (ex. number of unique classes in the target_array or directory)
        
        Keyword Arguments:
            image_data_generator {ImageDataGenerator} --
                A class which is the same as keras.preprocessing.image.ImageDataGenerator.
                If you know how to use keras, you can pass an argument you want.
                Otherwise, don't worry! Just pass this one.
                (default: {None})
            batch_size {int or None} --
                Number of samples per gradient update.
                If unspecified, batch_size will default to 32.
                If you don't know about batch size,
                just adjust this value to reduce a training time
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
                Decide whether using keras's fit_generator or not when the data are images.
                Check https://keras.io/models/model/ for usage.
                If you don't want to know how to use this one, then just pass.
                (default: {False})
        """
        if self.is_image_data == True:
            if type(image_data_generator) == type(None):
                train_datagen = self.create_image_data_generator(rescale = 1./255)
            else:
                train_datagen = image_data_generator
            self.train_with_images(train_datagen, batch_size, steps_per_epoch, epochs, verbose, callbacks, shuffle, use_fit_generator)
        else:
            if type(self.model) == type(None):
                unique_classes = numpy.lib.arraysetops.unique(self.target_array)
                class_indices = self.create_class_indices(unique_classes)
                num_classes = len(class_indices)
                self.init_class_dictionary_and_model(class_indices, num_classes)
                self.compile_model(optimizer = 'nadam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
            else:
                num_classes = self.model.output_shape[1]
            y_train = self.prepare_y(self.target_array, reverse_dict(self.class_dictionary), num_classes)
            self.model.fit(self.x_train, y_train, batch_size = batch_size, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
    
    def train_with_images(self, train_datagen, batch_size, steps_per_epoch, epochs, verbose, callbacks, shuffle, use_fit_generator):
        if use_fit_generator == False:
            if self.get_image_from == 'directory':
                images, classes = directory_images_to_arrays(self.data_path, self.input_shape[:2])
                self.prepare_train_data(is_image_data = True, get_image_from='argument', data_array=images, target_array=classes)
            
            if type(self.model) == type(None):
                unique_classes = numpy.lib.arraysetops.unique(self.target_array)
                class_indices = self.create_class_indices(unique_classes)
                num_classes = len(class_indices)
                self.init_class_dictionary_and_model(class_indices, num_classes)
                self.compile_model(optimizer = 'nadam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
            else:
                num_classes = self.model.output_shape[1]
            y_train = self.prepare_y(self.target_array, reverse_dict(self.class_dictionary), num_classes)
            self.model.fit(self.x_train, y_train, batch_size = batch_size, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
        else:
            if self.get_image_from == 'directory':
                train_generator = train_datagen.flow_from_directory(self.data_path, target_size = self.input_shape[:2], class_mode = 'categorical')
                if type(self.model) == type(None):
                    class_indices = train_generator.class_indices
                    self.init_class_dictionary_and_model(class_indices, len(class_indices))
                    self.compile_model(optimizer = 'nadam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
                self.model.fit_generator(train_generator, batch_size = batch_size, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
            elif self.get_image_from == 'argument':
                if type(self.model) == type(None):
                    unique_classes = numpy.lib.arraysetops.unique(self.target_array)
                    class_indices = self.create_class_indices(unique_classes)
                    num_classes = len(class_indices)
                    self.init_class_dictionary_and_model(class_indices, num_classes)
                    self.compile_model(optimizer = 'nadam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
                else:
                    num_classes = self.model.output_shape[1]
                y_train = self.prepare_y(self.target_array, reverse_dict(self.class_dictionary), num_classes)
                train_generator = train_datagen.flow(self.x_train, y_train)
                self.model.fit_generator(train_generator, batch_size = batch_size, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)

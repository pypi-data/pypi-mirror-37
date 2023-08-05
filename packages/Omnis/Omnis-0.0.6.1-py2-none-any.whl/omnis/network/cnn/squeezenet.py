"""SqueezeNet model

[a] keras-squeezenet
https://github.com/rcmalli/keras-squeezenet
"""

import keras
import cv2
import numpy as np

from keras.preprocessing.image import ImageDataGenerator
import keras_squeezenet

import os

from .cnn import CNN

class SqueezeNet(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        self.input_shape = (227, 227, 3)

    def __str__(self):
        return 'SqueezeNet'
    
    def create_model(self, num_classes):
        model = keras_squeezenet.SqueezeNet( weights=None, classes=num_classes )
        return model

if __name__ == '__main__':
    from keras.datasets import cifar10
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    cnn = SqueezeNet()
    cnn.prepare_data(is_image_data = True, get_image_from='argument', data_array=x_train, label_array=y_train)
    cnn.train(epochs = 1000, use_fit_generator = False)
    print('hi')
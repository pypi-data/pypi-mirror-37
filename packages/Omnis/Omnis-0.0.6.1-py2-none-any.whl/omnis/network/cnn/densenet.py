import keras

from keras.preprocessing.image import ImageDataGenerator

from keras.applications.densenet import DenseNet121
from keras.applications.densenet import DenseNet169
from keras.applications.densenet import DenseNet201

import os

from .cnn import CNN

class DenseNet(CNN):
    def __init__(self, model_path = None, depth = 121):
        """DenseNet models are initialized with the depth specified.
        
        Arguments:
            CNN {class} -- Superclass of CNN models. Users don't have pass it.
            
        Keyword Arguments:
            model_path {str} -- A path of model file. (default: {None})
            depth {int} -- Depth of DenseNet model. For now, you should choose among 121, 169 and 201. (default: {121})            
                
        Raises:
            ValueError -- Invalid depth value.
            e -- Raise ValueError.
        """
        CNN.__init__(self, model_path = model_path)
        try:
            if depth == 121:
                self.model_class = DenseNet121
            elif depth == 169:
                self.model_class = DenseNet169
            elif depth == 201:
                self.model_class = DenseNet201
            else:
                raise ValueError('no densenet model with the depth ' + str(depth) + ' exists')
            self.depth = depth
            self.input_shape = (224, 224, 3)
        except Exception as e:
            raise e

    def __str__(self):
        return 'DenseNet' + str(self.depth)
    
    def create_model(self, num_classes):
        model = self.model_class( weights=None, classes=num_classes )
        return model

if __name__ == '__main__':
    from keras.datasets import cifar10
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    cnn = DenseNet()
    cnn.prepare_data(is_image_data = True, get_image_from='argument', data_array=x_train, label_array=y_train)
    cnn.train(epochs = 100)
    print('hi')
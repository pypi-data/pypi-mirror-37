"""SqueezeNet model

[a] keras-squeezenet
https://github.com/rcmalli/keras-squeezenet
"""
import keras_squeezenet

from .cnn import CNN

class SqueezeNet(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        self.input_shape = (227, 227, 3)
    
    def create_model(self, num_classes):
        model = keras_squeezenet.SqueezeNet( weights=None, classes=num_classes )
        return model
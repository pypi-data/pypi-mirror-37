from keras.applications import xception

from .cnn import CNN

class Xception(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        if hasattr(self, 'input_shape') == False:
            self.input_shape = (299, 299, 3)
    
    def create_model(self, num_classes):
        model = xception.Xception( weights=None, input_shape=self.input_shape, classes=num_classes )
        return model
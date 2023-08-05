from keras.applications import nasnet

from .cnn import CNN

class NASNet_Large(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        if hasattr(self, 'input_shape') == False:
            self.input_shape = (331, 331, 3)
    
    def create_model(self, num_classes):
        model = nasnet.NASNetLarge( weights=None, input_shape=self.input_shape, classes=num_classes )
        return model
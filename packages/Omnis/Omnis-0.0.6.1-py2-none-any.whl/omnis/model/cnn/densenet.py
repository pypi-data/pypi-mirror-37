from keras.applications import densenet

from .cnn import CNN

class DenseNet121(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        self.input_shape = (224, 224, 3)
    
    def create_model(self, num_classes):
        model = densenet.DenseNet121( weights=None, classes=num_classes )
        return model

class DenseNet169(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        self.input_shape = (224, 224, 3)
    
    def create_model(self, num_classes):
        model = densenet.DenseNet169( weights=None, classes=num_classes )
        return model

class DenseNet201(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        self.input_shape = (224, 224, 3)
    
    def create_model(self, num_classes):
        model = densenet.DenseNet201( weights=None, classes=num_classes )
        return model
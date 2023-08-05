from keras.applications import resnet50

from .cnn import CNN

class ResNet50(CNN):
    def __init__(self, *args, **kwargs):
        CNN.__init__(self, *args, **kwargs)
        if hasattr(self, 'input_shape') == False:
            self.input_shape = (224, 224, 3)
    
    def create_model(self, num_classes):
        model = resnet50.ResNet50( weights=None, input_shape=self.input_shape, classes=num_classes )
        return model
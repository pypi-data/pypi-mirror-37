import numpy as np

class Rescale():
    def __init__(self, scale):
        self.scale = scale

    def __call__(self, image):
        return np.true_divide(image, self.scale)
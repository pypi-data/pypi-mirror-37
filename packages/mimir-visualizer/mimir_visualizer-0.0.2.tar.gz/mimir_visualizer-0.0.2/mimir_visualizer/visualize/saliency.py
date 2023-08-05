from keras.layers.convolutional import _Conv
from keras.layers.pooling import _Pooling2D

import keras.backend as K
import numpy as np

import cv2

from .class_activations import _gradcam_visualization

def _saliency_visualization(model, input_image,
    layer_index=None, layer_name=None):
    """
        Creates a saliency map using the guided backpropagation
        approach. Based on paper by Springenberg et al.

        # Source 
            https://arxiv.org/abs/1412.6806
    """

    K.set_learning_phase(0)

    input_layer = model.layers[0].input
    target_layer = model.get_layer(layer_name, layer_index).output

    loss = K.sum(K.max(target_layer, axis=3))
    saliency = K.gradients(loss, input_layer)[0]

    return K.function([input_layer], [saliency])([input_image])

def _deprocess_saliency(saliency_map):
    """ 
        Converts saliency map to viewable image.
    """
    
    if np.ndim(saliency_map) > 3:
        saliency_map = np.squeeze(saliency_map)

    saliency_map *= 255
    saliency_map = np.clip(saliency_map, 0, 255)

    return saliency_map

def generate_saliency(model, input_image, layer_index=None, 
    layer_name=None, backprop_modifiers=None, image_modifiers=None):
    """
        Helper function to generate saliency map.
    """

    input_size = tuple(model.input.shape[1:3])

    input_image = cv2.resize(input_image, input_size)
    input_image = np.reshape(input_image, (1, *input_size, 3))
    
    if layer_index is None and layer_name is None:
        for index in range(0, len(model.layers)):
            layer = model.layers[-index]
            if isinstance(layer, _Conv) or isinstance(layer, _Pooling2D):
                layer_name = layer.name
                break

    if backprop_modifiers is not None:
        model = backprop_modifiers(model)

    saliency_map = _saliency_visualization(model, 
        input_image.astype(np.float32), layer_index, layer_name)
    saliency_map = _deprocess_saliency(saliency_map)

    return saliency_map

def generate_class_saliency(model, input_image, class_index=None, 
    layer_index=None, layer_name=None, backprop_modifiers=None,
    image_modifiers=None):
    """
        Creates the class specific saliency map by combining the 
        class specific gradient weighted class activation map with a 
        guided backpropagation based saliency map. Based on paper by 
        Selvaraju et al.

        # Source 
            https://arxiv.org/abs/1610.02391
    """

    input_size = tuple(model.input.shape[1:3])

    input_image = cv2.resize(input_image, input_size)
    input_image = np.reshape(input_image, (1, *input_size, 3))
    
    if layer_index is None and layer_name is None:
        for index in range(0, len(model.layers)):
            layer = model.layers[-index]
            if isinstance(layer, _Conv) or isinstance(layer, _Pooling2D):
                layer_name = layer.name
                break

    cam = _gradcam_visualization(model, input_image.astype(np.float32), 
        class_index, layer_index, layer_name)
    cam = cam[..., np.newaxis]

    if backprop_modifiers is not None:
        model = backprop_modifiers(model)

    saliency = _saliency_visualization(model, input_image.astype(np.float32), 
        layer_index, layer_name)
    saliency = np.squeeze(saliency)

    class_saliency_map = saliency * cam
    class_saliency_map =_deprocess_saliency(class_saliency_map)

    return class_saliency_map
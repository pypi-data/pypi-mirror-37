from keras.layers import Activation, GlobalAveragePooling2D
from .class_activations import _gradcam_visualization

import keras.backend as K
import tensorflow as tf
import numpy as np
import cv2

def _saliency_visualization(model, input_image,
    layer_index=None, layer_name=None):
    """
        Creates the saliency map representation of the given image
        at the point of the given layer_id.

        # Arguments
            model:
            input_image: 
            layer_index: 
            layer_name:
    """

    with tf.get_default_graph().gradient_override_map({'Relu': 'GuidedRelu'}):
        
        input_layer = model.layers[0].input
        target_layer = model.get_layer(layer_name, layer_index).output

        loss = K.sum(K.max(target_layer, axis=3))
        saliency = K.gradients(loss, input_layer)[0]

        return K.function([input_layer], [saliency])([input_image])

def _guided_gradcam_visualization(model, input_image, class_index=None,
        layer_index=None, layer_name=None):
    """
        Creates the saliency map representation of the given image
        at the point of the given layer_id.

        # Arguments
            model:
            class_index:
            input_image: 
            layer_index: 
            layer_name:
    """

    saliency = _saliency_visualization(model, input_image, 
        layer_index, layer_name)
    saliency = np.squeeze(saliency)

    cam = _gradcam_visualization(model, input_image, 
        class_index, layer_index, layer_name)
    cam = cam[..., np.newaxis]

    return saliency * cam

def _deprocess_guided_gradcam(image):
    """
    
    """
    
    if np.ndim(image) > 3:
        image = np.squeeze(image)
        
    image -= image.mean()
    image /= (image.std() + 1e-5)
    image *= 0.1

    image += 0.5
    image = np.clip(image, 0, 1)

    image *= 255
    
    image = np.clip(image, 0, 255).astype('uint8')
    return image

def _deprocess_saliency(saliency_map):
    """ 

    """
    
    if np.ndim(saliency_map) > 3:
        saliency_map = np.squeeze(saliency_map)

    saliency_map *= 255
    saliency_map = np.clip(saliency_map, 0, 255)

    return saliency_map

def generate_saliency(model, input_image, layer_index=None, 
    layer_name=None, backprop_modifiers=None, image_modifications=None):
    """

    """

    input_size = tuple(model.input.shape[1:3])

    input_image = cv2.resize(input_image, input_size)
    input_image = np.reshape(input_image, (1, *input_size, 3))

    if backprop_modifiers is not None:
        model = backprop_modifiers()(model)

    saliency_map = _saliency_visualization(model, 
        input_image.astype(np.float32), layer_index, layer_name)
    saliency_map = _deprocess_guided_gradcam(saliency_map)

    if image_modifications is not None:
        saliency_map = image_modifications()(saliency_map)

    return saliency_map

def generate_class_saliency(model, input_image, class_index=None, 
    layer_index=None, layer_name=None, backprop_modifiers=None,
    image_modifications=None):
    """

    """

    input_size = tuple(model.input.shape[1:3])

    input_image = cv2.resize(input_image, input_size)
    input_image = np.reshape(input_image, (1, *input_size, 3))

    if backprop_modifiers is not None:
        model = backprop_modifiers()(model)

    class_saliency_map = _guided_gradcam_visualization(model, 
        input_image.astype(np.float32), class_index, layer_index, layer_name)

    class_saliency_map =_deprocess_saliency(class_saliency_map)

    if image_modifications is not None:
        class_saliency_map = image_modifications()(class_saliency_map)

    return class_saliency_map
from keras.layers import Activation, GlobalAveragePooling2D
from keras.layers.convolutional import _Conv
from keras.layers.pooling import _Pooling2D

import keras.backend as K
import numpy as np

import cv2

def _gradcam_visualization(model, input_image, class_index=None, 
    layer_index=None, layer_name=None):
    """
        
    """

    input_layer = model.layers[0].input
    output_layer = model.layers[-1].output
    target_layer = model.get_layer(layer_name, layer_index).output

    number_of_classes = int(output_layer.shape[1])

    loss = K.sum(output_layer * K.one_hot([class_index], number_of_classes))

    gradients = K.gradients(loss, target_layer)[0]
    gradients /= (K.sqrt(K.mean(K.square(gradients))) + K.epsilon())

    weights = GlobalAveragePooling2D()(gradients)

    gradcam = K.sum(weights * target_layer, axis=-1)
    gradcam = Activation('relu')(gradcam)

    gradcam_fn = K.function([input_layer], [gradcam])

    gradcam = gradcam_fn([input_image])
    gradcam = cv2.resize(np.squeeze(gradcam), tuple(input_layer.shape[1:3]))

    return gradcam / np.max(gradcam)

def _deprocess_gradcam(image, gradcam):
    """
    
    """
    
    if np.ndim(image) > 3:
        image = np.squeeze(image)

    image -= np.min(image)     
    image  = np.minimum(image, 255)

    gradcam = cv2.applyColorMap(np.uint8(255 * gradcam), cv2.COLORMAP_JET)
    gradcam = np.float32(gradcam) + np.float32(image)
    gradcam = 255 * gradcam / np.max(gradcam)

    gradcam = cv2.cvtColor(gradcam, cv2.COLOR_BGR2RGB)

    return gradcam

def generate_gradcam(model, input_image, class_index=None, 
    layer_index=None, layer_name=None, image_modifiers=None, 
    backprop_modifiers=None):
    """

    """

    input_size = tuple(model.input.shape[1:3])

    input_image = cv2.resize(input_image, input_size)
    input_image = np.reshape(input_image, (1, *input_size, 3))
    source_image = input_image

    if layer_index is None and layer_name is None:
        for index in range(0, len(model.layers)):
            layer = model.layers[-index]
            if isinstance(layer, _Conv) or isinstance(layer, _Pooling2D):
                layer_name = layer.name
                break

    if image_modifiers is not None:
        input_image = image_modifiers(input_image)

    if backprop_modifiers is not None:
        model = backprop_modifiers(model)

    gradcam = _gradcam_visualization(model, input_image.astype(np.float32),
        class_index, layer_index, layer_name)

    return  _deprocess_gradcam(source_image, gradcam)
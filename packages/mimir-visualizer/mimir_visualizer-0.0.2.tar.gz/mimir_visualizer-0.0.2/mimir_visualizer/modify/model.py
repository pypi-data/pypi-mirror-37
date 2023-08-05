from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_nn_ops
from keras.models import load_model, clone_model

import tensorflow as tf

import os
import tempfile

def temppath(filename):
    return os.path.join(tempfile.gettempdir(), filename)

def clone(model):
    temp_path = temppath('temp_model')
    model.save(temp_path)
    model_clone = load_model(temp_path)
    os.remove(temp_path)
    return model_clone

class GuidedBackprop():

    def __call__(self, model):
        with tf.get_default_graph().gradient_override_map({'Relu': 'GuidedRelu'}):

            model = clone(model)

            for layer in model.layers[1:]:
                if hasattr(layer, 'activation'):
                    layer.activation = tf.nn.relu

            return model
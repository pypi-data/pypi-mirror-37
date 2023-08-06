# MIT License
# 
# Copyright (c) 2018 Michael Fuerst
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import tensorflow as tf
from starttf.models.model import StartTFModel


class TFHubWrapper(StartTFModel):
    def __init__(self, hyperparams):
        super(TFHubWrapper, self).__init__(hyperparams)
        self.module = tf.contrib.hub.Module(hyperparams.tf_hub_wrapper.model_url, trainable=hyperparams.tf_hub_wrapper.trainable)

    def call(self, input_tensor, training=False):
        model = {}
        debug = {}
        with tf.variable_scope('tf_hub_wrapper'):
            image = tf.cast(input_tensor["image"], dtype=tf.float32, name="input/cast")
            model["output"] = self.module(image / 255.0)
            debug["image"] = image
        return model, debug

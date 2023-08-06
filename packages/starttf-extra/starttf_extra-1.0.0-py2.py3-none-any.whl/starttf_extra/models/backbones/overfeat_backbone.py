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

from starttf.models.model import StartTFPartialModel
from starttf.layers.tile_2d import tile_2d

class OverfeatBackbone(StartTFPartialModel):
    def __init__(self, hyperparams):
        super(OverfeatBackbone, self).__init__(hyperparams)

    def call(self, input_tensor, training=False):
        model = {}
        debug = {}
        tmp = input_tensor["pool5"]
        tmp = tf.layers.conv2d(inputs=tmp, filters=4096, kernel_size=(conv6_size, conv6_size),
                                        strides=(1, 1), padding="same", activation=tf.nn.relu, name="conv6")
        tmp = tf.layers.conv2d(inputs=tmp, filters=4096, kernel_size=(1, 1), strides=(1, 1),
                                          padding="valid", activation=tf.nn.relu, name="conv7")

        tile = self.hyperparams.backbone.get("tiling", 8)
        model["conv7_tiled"] = tile_2d(tmp, tile, tile, "conv7_tiled")

        return model, debug

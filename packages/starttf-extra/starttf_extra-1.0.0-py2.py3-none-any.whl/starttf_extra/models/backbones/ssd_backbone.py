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
from starttf.layers.normalization import L2Normalization


Conv2D = tf.keras.layers.Conv2D
ZeroPadding2D = tf.keras.layers.ZeroPadding2D
l2 = tf.keras.regularizers.l2


class SSDBackbone(StartTFPartialModel):
    def __init__(self, hyperparams):
        super(SSDBackbone, self).__init__(hyperparams)

    def call(self, input_tensor, training=False):
        """
        Run the model.

        Required: input_tensor = {"conv4_3", "pool5"}
        Output: {"conv4_3_norm", "fc7", "conv_{6...}_2"}
        """
        model = {}
        debug = {}

        # Some helper variables for convenience.
        feature_size = self.hyperparams.backbone.get("feature_size", 256)
        feature_size_2 = int(feature_size / 2)
        reg = self.hyperparams.backbone.get("regularization", 0.0005)

        # Make a highres output before pool5 of vgg. SSD default is true.
        if self.hyperparams.backbone.get("high_res", True):
            conv4_3 = input_tensor["conv4_3"]
            conv4_3_norm = L2Normalization(gamma_init=20, name='conv4_3_norm')(conv4_3)
            model["conv4_3_norm"] = conv4_3_norm

        # Normal VGG sized output.
        pool5 = input_tensor["pool5"]
        fc6 = Conv2D(1024, (3, 3), dilation_rate=(6, 6), activation='relu', padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='fc6')(pool5)
        fc7 = Conv2D(1024, (1, 1), activation='relu', padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='fc7')(fc6)
        model["fc7"] = fc7

        ###################################################################
        # Add extra conf layers to vgg backbone. SSD300 is 4 SSD512 is 5. #
        ###################################################################
        if (self.hyperparams.backbone.get("extra_conf_levels", 4)) >= 1:
            conv6_1 = Conv2D(feature_size, (1, 1), activation='relu', padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='conv6_1')(fc7)
            conv6_1 = ZeroPadding2D(padding=((1, 1), (1, 1)), name='conv6_padding')(conv6_1)
            conv6_2 = Conv2D(2 * feature_size, (3, 3), strides=(2, 2), activation='relu', padding='valid', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='conv6_2')(conv6_1)
            model["conv6_2"] = conv6_2

        if (self.hyperparams.backbone.get("extra_conf_levels", 4)) >= 2:
            conv7_1 = Conv2D(feature_size_2, (1, 1), activation='relu', padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='conv7_1')(conv6_2)
            conv7_1 = ZeroPadding2D(padding=((1, 1), (1, 1)), name='conv7_padding')(conv7_1)
            conv7_2 = Conv2D(feature_size, (3, 3), strides=(2, 2), activation='relu', padding='valid', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='conv7_2')(conv7_1)
            model["conv7_2"] = conv7_2

        # Further layers are all similar, so create them in a loop for flexibility.
        if (self.hyperparams.backbone.get("extra_conf_levels", 4)) >= 3:
            tmp = model["conv7_2"]
            for i in range(self.hyperparams.backbone.get("extra_conf_levels", 4) - 2):
                tmp = Conv2D(feature_size_2, (1, 1), activation='relu', padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='conv{}_1'.format(8+i))(tmp)
                tmp = Conv2D(feature_size, (3, 3), strides=(1, 1), activation='relu', padding='valid', kernel_initializer='he_normal', kernel_regularizer=l2(reg), name='conv{}_2'.format(8+i))(tmp)
                model['conv{}_2'.format(8+i)] = tmp

        return model, debug

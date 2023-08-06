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
from starttf.layers.upsamling import UpsampleLike

Conv2D = tf.keras.layers.Conv2D
Add = tf.keras.layers.Add
Activation = tf.keras.layers.Activation


class FPNBackbone(StartTFPartialModel):
    def __init__(self, hyperparams):
        super(FPNBackbone, self).__init__(hyperparams)

    def call(self, input_tensor, training=False):
        """
        Run the model.
        """
        model = {}
        debug = {}
        feature_size = self.hyperparams.backbone.get("feature_size", 256)

        prev = None
        # Build feature pyramid similar to detectron
        for i in range(len(input_tensor)):
            fpn_idx = len(input_tensor) - i - 1

            # Lateral connection
            tmp = Conv2D(feature_size, kernel_size=1, strides=1, padding='same', name='fpn_{}_reduced'.format(fpn_idx))(input_tensor[fpn_idx])

            # Merge with previous upsampled (smaller resolution) layer
            if prev is not None:
                tmp = Add(name='fpn_{}_merged'.format(fpn_idx))([prev, tmp])

            # Upsample layer
            if fpn_idx - 1 >= 0:
                larger_scale_input = input_tensor[fpn_idx - 1]
                prev = UpsampleLike(name='fpn_{}_upsampled'.format(fpn_idx))([tmp, larger_scale_input])

            # Make feature output for this resolution
            # FIXME Why does there seem to be no activation in detectron? Having no activation here seems stupid.
            model['fpn_{}'.format(fpn_idx)] = Conv2D(feature_size, kernel_size=3, strides=1, padding='same', name='fpn_{}'.format(fpn_idx))(tmp)

        # Coarser FPN levels introduced for RetinaNet (like in detectron code)
        # Basically adds relu, conv blocks to network. Note how relu is first, since output layers should not have a
        # non-linearity.
        if self.hyperparams.backbone.get("extra_conf_levels", 0) > 0:
            tmp = input_tensor[-1]
            for i in range(self.hyperparams.backbone.get("extra_conf_levels", 0)):
                # If not first output layer add non-linearity. First output already has non-linearity from encoder.
                if i > 0:
                    name = "fpn_{}_relu".format(i + normal_conv_levels + 1)
                    tmp = Activation('relu', name=name)(tmp)
                # Add a conv that is output ready
                name = "fpn_{}".format(i + normal_conv_levels + 1)
                tmp = Conv2D(feature_size, kernel_size=3, strides=2, padding='same', name=name)(tmp)
                model[name] = tmp

        return model, debug

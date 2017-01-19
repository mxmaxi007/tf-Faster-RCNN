# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 20:11:09 2017

@author: Kevin Liang

The ResNet50 Architecture: Convolutional feature extractor

Built on TensorBase: https://github.com/kevinjliang/TensorBase
"""
import sys
sys.path.append('../')

from Lib.TensorBase.tensorbase.base import Layers

import tensorflow as tf

class resnet50:
    def __init__(self, x):
        self.network = self._network(x)
        self._feat_stride = 2**5        # Total downsampling factor of the network
        
    def _network(self, x):
        conv_layers = Layers(x)
            
        # Convolutional layers
        with tf.variable_scope('resnet50'):
            res_blocks = [1,3,4,6,3]
            output_channels = [64,256,512,1024,2048]
            
            with tf.variable_scope('scale0'):
                conv_layers.conv2d(filter_size=7, output_channels=output_channels[0], stride=2, padding='SAME', b_value=None)
                conv_layers.maxpool(k=3,s=2)
            with tf.variable_scope('scale1'):
                conv_layers.res_layer(filter_size=3, output_channels=output_channels[1], stride=2)
                for block in range(res_blocks[1]-1):
                    conv_layers.res_layer(filter_size=3, output_channels=output_channels[1], stride=1)
            with tf.variable_scope('scale2'):
                conv_layers.res_layer(filter_size=3, output_channels=output_channels[2], stride=2)
                for block in range(res_blocks[2]-1):
                    conv_layers.res_layer(filter_size=3, output_channels=output_channels[2], stride=1)
            with tf.variable_scope('scale3'):
                conv_layers.res_layer(filter_size=3, output_channels=output_channels[3], stride=2)
                for block in range(res_blocks[3]-1):
                    conv_layers.res_layer(filter_size=3, output_channels=output_channels[3], stride=1)
            with tf.variable_scope('scale4'):
                conv_layers.res_layer(filter_size=3, output_channels=output_channels[4], stride=2)
                for block in range(res_blocks[4]-1):
                    conv_layers.res_layer(filter_size=3, output_channels=output_channels[4], stride=1)
        
        return conv_layers
        
    def get_output(self):
        return self.network.get_output()
        
    def get_feat_stride(self):
        return self._feat_stride
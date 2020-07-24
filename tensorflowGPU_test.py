# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:17:22 2020

@author: Administrator
"""
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
hello = tf.constant('Hello, TensorFlow!')
config = tf.compat.v1.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.9
sess = tf.compat.v1.Session()
print(sess.run(hello))
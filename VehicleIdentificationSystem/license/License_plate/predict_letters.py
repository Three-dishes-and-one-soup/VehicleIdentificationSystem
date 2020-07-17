# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:12:05 2020

@author: lenovo
"""


 
import numpy as np
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from PIL import Image
import os
 
 

 


# 定义卷积函数
def conv_layer(inputs, W, b, conv_strides, kernel_size, pool_strides, padding):
    L1_conv = tf.nn.conv2d(inputs, W, strides=conv_strides, padding=padding)
    L1_relu = tf.nn.relu(L1_conv + b)
    return tf.nn.max_pool(L1_relu, ksize=kernel_size, strides=pool_strides, padding='SAME')
 
# 定义全连接层函数
def full_connect(inputs, W, b):
    return tf.nn.relu(tf.matmul(inputs, W) + b)
 
    
 
    
 
def predict():    
#if __name__ =='__main__' and sys.argv[1]=='predict':
    license_num = ""
    SIZE = 1280
    WIDTH = 32
    HEIGHT = 40
    NUM_CLASSES = 26

    SAVER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'License_plate/train-saver/letters/')
 
    LETTERS = ("A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V","W","X","Y","Z","I","O")


# 定义输入节点，对应于图片像素值矩阵集合和图片标签(即所代表的数字)
    x = tf.placeholder(tf.float32, shape=[None, SIZE])
    y_ = tf.placeholder(tf.float32, shape=[None, NUM_CLASSES])
 
    x_image = tf.reshape(x, [-1, WIDTH, HEIGHT, 1])
    saver = tf.train.import_meta_graph("%smodel.ckpt.meta"%(SAVER_DIR))
    with tf.Session() as sess:
        model_file=tf.train.latest_checkpoint(SAVER_DIR)
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())
        saver.restore(sess, model_file)
 
        # 第一个卷积层
        W_conv1 = sess.graph.get_tensor_by_name("W_conv1:0")
        b_conv1 = sess.graph.get_tensor_by_name("b_conv1:0")
        conv_strides = [1, 1, 1, 1]
        kernel_size = [1, 2, 2, 1]
        pool_strides = [1, 2, 2, 1]
        L1_pool = conv_layer(x_image, W_conv1, b_conv1, conv_strides, kernel_size, pool_strides, padding='SAME')
 
        # 第二个卷积层
        W_conv2 = sess.graph.get_tensor_by_name("W_conv2:0")
        b_conv2 = sess.graph.get_tensor_by_name("b_conv2:0")
        conv_strides = [1, 1, 1, 1]
        kernel_size = [1, 1, 1, 1]
        pool_strides = [1, 1, 1, 1]
        L2_pool = conv_layer(L1_pool, W_conv2, b_conv2, conv_strides, kernel_size, pool_strides, padding='SAME')
 
 
        # 全连接层
        W_fc1 = sess.graph.get_tensor_by_name("W_fc1:0")
        b_fc1 = sess.graph.get_tensor_by_name("b_fc1:0")
        h_pool2_flat = tf.reshape(L2_pool, [-1, 16 * 20*32])
        h_fc1 = full_connect(h_pool2_flat, W_fc1, b_fc1)
 
 
        # dropout
        keep_prob = tf.placeholder(tf.float32)
 
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
 
 
        # readout层
        W_fc2 = sess.graph.get_tensor_by_name("W_fc2:0")
        b_fc2 = sess.graph.get_tensor_by_name("b_fc2:0")
 
        # 定义优化器和训练op
        conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
 
        for n in range(2,3):
            path = "./cache/%s.bmp" % (n)
            img = Image.open(path)
            width = img.size[0]
            height = img.size[1]
 
            img_data = [[0]*SIZE for i in range(1)]
            for h in range(0, height):
                for w in range(0, width):
                    if img.getpixel((w, h)) < 190:
                        img_data[0][w+h*width] = 1
                    else:
                        img_data[0][w+h*width] = 0
            
            result = sess.run(conv, feed_dict = {x: np.array(img_data), keep_prob: 1.0})
            
            max1 = 0
            max2 = 0
            max3 = 0
            max1_index = 0
            max2_index = 0
            max3_index = 0
            for j in range(NUM_CLASSES):
                if result[0][j] > max1:
                    max1 = result[0][j]
                    max1_index = j
                    continue
                if (result[0][j]>max2) and (result[0][j]<=max1):
                    max2 = result[0][j]
                    max2_index = j
                    continue
                if (result[0][j]>max3) and (result[0][j]<=max2):
                    max3 = result[0][j]
                    max3_index = j
                    continue
            
            if n == 3:
                license_num += "-"
            license_num = license_num + LETTERS[max1_index]
#            print ("概率：  [%s %0.2f%%]    [%s %0.2f%%]    [%s %0.2f%%]" % (LETTERS_DIGITS[max1_index],max1*100, LETTERS_DIGITS[max2_index],max2*100, LETTERS_DIGITS[max3_index],max3*100))
            
#        print ("城市代号是: 【%s】" % license_num)
        return max1_index, max1, max2_index, max2, max3_index, max3
    
    

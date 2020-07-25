'''
author: 翁玮熙
create time: 2020/7/21
update time: 2020/7/23
'''
name=['喝水', '正常驾驶', '左手打电话', '左手玩手机', '梳妆整理', '调校广播', '右手打电话', '右手玩手机',
             '从后面拿东西', '和客人讲话']

import numpy as np
import tensorflow as tf
def apiRequest(image_Path):
    #cv2.imshow('',img)
    #cv2.waitKey(0)
    requestData={}
    model=tf.keras.models.load_model('driveractions/model/my_model3')
    model.compile("adam", "categorical_crossentropy", ['accuracy'])
    image = tf.compat.v1.read_file(image_Path)
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.cast(image, tf.float32)
    image = (image / 127.5) - 1
    image = tf.image.resize(image, (160, 160))
    images = [image]
    output = model.predict(np.array(images), batch_size=1)
    pro = output.max()
    index = output.argmax()
    requestData={"type": (name[index]), "probability":str(pro)}
    return requestData

# def onlineRequest(image_Path):
#     model=tf.keras.models.load_model('my_model3')
#     model.compile("adam", "categorical_crossentropy", ['accuracy'])
#     image = tf.compat.v1.read_file(image_Path)
#     image = tf.image.decode_jpeg(image, channels=3)
#     image = tf.cast(image, tf.float32)
#     image = (image / 127.5) - 1
#     image = tf.image.resize(image, (160, 160))
#     images = [image]
#     output = model.predict(np.array(images), batch_size=1)
#     index = output.argmax()
#     return name[index]
#
# onlineRequest('./test1.jpg')
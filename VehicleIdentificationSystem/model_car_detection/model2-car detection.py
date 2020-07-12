# -*- coding: utf-8 -*-
"""
author: 翁玮熙
create ：time：2020-07-08
update ：time：2020-07-11
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
AUTOTUNE = tf.data.experimental.AUTOTUNE
import pathlib
data_root =  pathlib.Path('D:/BaiduNetdiskDownload/train-1/train')
val_root= pathlib.Path('D:/BaiduNetdiskDownload/train-1/validation')
print(data_root)

for item in data_root.iterdir():
  print(item)

import random
all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]
random.shuffle(all_image_paths)

image_count = len(all_image_paths)
print(image_count)

for item in val_root.iterdir():
  print(item)
  
import random
val_image_paths = list(val_root.glob('*/*'))
val_image_paths = [str(path) for path in val_image_paths]
random.shuffle(val_image_paths)

image_val_count = len(val_image_paths)
print(image_val_count)
  
label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())
print(label_names)

label_to_index = dict((name, index) for index, name in enumerate(label_names))
print(label_to_index)

all_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                    for path in all_image_paths]

label_names = sorted(item.name for item in val_root.glob('*/') if item.is_dir())
print(label_names)

label_to_index = dict((name, index) for index, name in enumerate(label_names))
print(label_to_index)

val_image_labels = [label_to_index[pathlib.Path(path).parent.name]
                    for path in val_image_paths]

print("First 10 labels indices: ", all_image_labels[:10])
print("First 10 labels indices: ", val_image_labels[:10])

img_path = all_image_paths[0]
img_raw = tf.io.read_file(img_path)
print(img_path)
print(repr(img_raw)[:100]+"...")

img_tensor = tf.image.decode_image(img_raw)

img_final = tf.image.resize(img_tensor, [192, 192])
img_final = img_final/255.0


def preprocess_image(image):
  image = tf.image.decode_jpeg(image, channels=3)
  image = tf.image.resize(image, [192, 192])
  image /= 255.0  # normalize to [0,1] range
  return image

def load_and_preprocess_image(path):
  image = tf.io.read_file(path)
  return preprocess_image(image)

path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)

print(path_ds)

image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)

label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))

for label in label_ds.take(10):
  print(label_names[label.numpy()])

image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))
#print(image_label_ds)

ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))

# 元组被解压缩到映射函数的位置参数中
def load_and_preprocess_from_path_label(path, label):
  return load_and_preprocess_image(path), label

image_label_ds = ds.map(load_and_preprocess_from_path_label)

BATCH_SIZE = 32

# 设置一个和数据集大小一致的 shuffle buffer size（随机缓冲区大小）以保证数据
# 被充分打乱。
ds = image_label_ds.shuffle(buffer_size=image_count)
ds = ds.repeat()
ds = ds.batch(BATCH_SIZE)
# 当模型在训练的时候，`prefetch` 使数据集在后台取得 batch。
ds = ds.prefetch(buffer_size=AUTOTUNE)



ds = image_label_ds.apply(
  tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
ds = ds.batch(BATCH_SIZE)
ds = ds.prefetch(buffer_size=AUTOTUNE)
mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
mobile_net.trainable=False
#help(keras_applications.mobilenet_v2.preprocess_input)

def change_range(image,label):
  return 2*image-1, label

keras_ds = ds.map(change_range)

model = tf.keras.Sequential([
  mobile_net,
  tf.keras.layers.GlobalAveragePooling2D(),
  tf.keras.layers.Dense(len(label_names), activation = 'softmax')])

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=["accuracy"])

model.summary()

steps_per_epoch=tf.math.ceil(len(all_image_paths)/BATCH_SIZE).numpy()

model.fit(ds, epochs=5, steps_per_epoch=steps_per_epoch)
'''
#keras_model_path = "/models"
saved_model_path = "/tmp/tf_save"
model = tf.keras.models.load_model(saved_model_path)
img_path = 'D:\BaiduNetdiskDownload\train-1\validation\family sedan\5c96b80615560aa2daded5378f0ddbc1.jpg'
img_raw = tf.io.read_file(img_path)
print(repr(img_raw)[:100]+"...")
image = tf.image.decode_jpeg(img_raw, channels=3)
image = tf.image.resize(image, [192, 192])
image /= 255.0  # normalize to [0,1] range

model.predict(image)
'''

'''
img =  'D:\BaiduNetdiskDownload\train-1\validation\family sedan\5c96b80615560aa2daded5378f0ddbc1.jpg'

img_final1 = load_and_preprocess_image(img_path1)
# 图像预处理

from keras.preprocessing import image
image_path =  'D:\BaiduNetdiskDownload\train-1\validation\family sedan\5c96b80615560aa2daded5378f0ddbc1.jpg'

# 加载图像
img = image.load_img(image_path, target_size=(192, 192))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

# 对图像进行分类
preds = model.predict(x)

# 输出预测概率
print( 'Predicted:', preds)
'''
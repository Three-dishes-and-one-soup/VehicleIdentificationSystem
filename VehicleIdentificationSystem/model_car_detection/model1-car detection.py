# -*- coding: utf-8 -*-
"""
author: 翁玮熙
create time：2020-07-08
update time：2020-07-11
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import numpy as np
#import matplotlib.pyplot as plt

import os
import PIL

train_dir = 'D:/BaiduNetdiskDownload/train-1/train'
val_dir = 'D:/BaiduNetdiskDownload/train-1/validation'
'''
creat_dataset.py
功能：change the size of pictures in one folder"
'''
'''


'''
train_bus_dir = os.path.join(train_dir, 'bus')  # directory with our training cat pictures
train_family_sedan_dir = os.path.join(train_dir, 'family sedan')  # directory with our training dog pictures
train_fire_engine_dir = os.path.join(train_dir, 'fire engine')
train_heavy_truck_dir = os.path.join(train_dir, 'heavy truck')
train_jeep_dir = os.path.join(train_dir, 'jeep') 
train_minibus_dir = os.path.join(train_dir, 'minibus') 
train_racing_car_dir = os.path.join(train_dir, 'racing car') 
train_suv_dir = os.path.join(train_dir, 'SUV') 
train_taxi_dir = os.path.join(train_dir, 'taxi') 
train_truck_dir = os.path.join(train_dir, 'truck') 

val_bus_dir = os.path.join(val_dir, 'bus')  # directory with our training cat pictures
val_family_sedan_dir = os.path.join(val_dir, 'family sedan')  # directory with our training dog pictures
val_fire_engine_dir = os.path.join(val_dir, 'fire engine')
val_heavy_truck_dir = os.path.join(val_dir, 'heavy truck')
val_jeep_dir = os.path.join(val_dir, 'jeep') 
val_minibus_dir = os.path.join(val_dir, 'minibus') 
val_racing_car_dir = os.path.join(val_dir, 'racing car') 
val_suv_dir = os.path.join(val_dir, 'SUV') 
val_taxi_dir = os.path.join(val_dir, 'taxi') 
val_truck_dir = os.path.join(val_dir, 'truck') 

num_bus_tr = len(os.listdir(train_bus_dir))
num_family_sedan_tr = len(os.listdir(train_family_sedan_dir))
num_fire_engine_tr = len(os.listdir(train_fire_engine_dir))
num_heavy_truck_tr = len(os.listdir(train_heavy_truck_dir))
num_jeep_tr = len(os.listdir(train_jeep_dir))
num_minibus_tr = len(os.listdir(train_minibus_dir))
num_racing_car_tr = len(os.listdir(train_racing_car_dir))
num_suv_tr = len(os.listdir(train_suv_dir))
num_taxi_tr = len(os.listdir(train_taxi_dir))
num_truck_tr = len(os.listdir(train_truck_dir))

num_bus_val = len(os.listdir(val_bus_dir))
num_family_sedan_val = len(os.listdir(val_family_sedan_dir))
num_fire_engine_val = len(os.listdir(val_fire_engine_dir))
num_heavy_truck_val= len(os.listdir(val_heavy_truck_dir))
num_jeep_val = len(os.listdir(val_jeep_dir))
num_minibus_val = len(os.listdir(val_minibus_dir))
num_racing_car_val = len(os.listdir(val_racing_car_dir))
num_suv_val = len(os.listdir(val_suv_dir))
num_taxi_val = len(os.listdir(val_taxi_dir))
num_truck_val = len(os.listdir(val_truck_dir))

total_train = num_bus_tr + num_family_sedan_tr+num_fire_engine_tr+num_heavy_truck_tr+num_jeep_tr+num_minibus_tr+num_racing_car_tr+num_suv_tr+num_taxi_tr+num_truck_tr
total_val = num_bus_val + num_family_sedan_val+num_fire_engine_val+num_heavy_truck_val+num_jeep_val+num_minibus_val+num_racing_car_val+num_suv_val+num_taxi_val+num_truck_val
print("Total training images:", total_train)
print("Total validation images:", total_val)

batch_size =128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150

train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=val_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')
sample_training_images, _ = next(train_data_gen)

# This function will plot images in the form of a grid with 1 row and 5 columns where images are placed in each column.
def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()
    



model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1)
])


#plotImages(sample_training_images[:5])


model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()

history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)


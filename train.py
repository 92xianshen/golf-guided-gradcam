'''
This code is for training a ConvNet on the normalized dataset
GAP layer is not used
'''
import os
import numpy as np
import tensorflow as tf
from model.GolfVGG import create_convnet

# Task
task = ('All', '645') # full time resolution
# task = ('All', '600')
# task = ('All', '550')
# task = ('All', '500')
# task = ('All', '450')

# Create result folder
result_path = 'saved_model/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

# Sensor and length selections
sensor_set = {
    'All'   : [0, 1, 2, 3, 4, 5, 6, 7], # SG + Acc. + Gyro.
    'SG'    : [0, 1],                   # SG
    'Acc.'  : [2, 3, 4],                # Acc.
    'Gyro.' : [5, 6, 7],                # Gyro.
}

sample_set = {
    '645': [350, 995], # 645
    '600': [350, 950], # 600
    '550': [350, 900], # 550
    '500': [350, 850], # 500
    '450': [350, 800], # 450
}

sensor, sample = sensor_set[task[0]], sample_set[task[1]]

# Create model
model = create_convnet(input_shape=[sample[1] - sample[0], len(sensor)])
model.compile(
    optimizer='Adam', 
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), 
    metrics=['accuracy'])

# Read dataset
x_train = np.load('../dataset/normalized/X_train_norm.npz')['arr_0']
y_train = np.load('../dataset/normalized/y_train.npz')['arr_0']

x_test = np.load('../dataset/normalized/X_test_norm.npz')['arr_0']
y_test = np.load('../dataset/normalized/y_test.npz')['arr_0']

# Training and test sets
x_training, y_training = x_train[..., sample[0]:sample[1], sensor], y_train
x_testing, y_testing = x_test[..., sample[0]:sample[1], sensor], y_test

model.fit(
    x_training, y_training, 
    epochs=100, 
    validation_data=(x_testing, y_testing))

model.save(
    os.path.join(
        result_path, 'convnet_{}_{}.h5'.format(
            task[0], task[1])))
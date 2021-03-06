import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from alexnet import alexnet
from mobilenet import MobileNet
from keras.callbacks import ModelCheckpoint
import tensorflow as tf
import os
import keras

WIDTH = 320
HEIGHT = 240
LR = 1e-3
EPOCHS = 75
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data'.format(LR, 'mobilenet',EPOCHS)
n_btch = 15


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

img_input = keras.layers.Input(shape=(WIDTH, HEIGHT, 3))
model = MobileNet(input_tensor=img_input,classes=9) ##alexnet(WIDTH, HEIGHT, LR, output = 4)
model.load_weights('weights/' + MODEL_NAME+ '.hdf5')

for epoch in range(EPOCHS):
    print('\n================================================ Epoch : {}/{} ================================================'. format(epoch + 1, EPOCHS))    
    for filename in os.listdir(os.getcwd() + '/data/'):
        train_data = np.load('data/' + filename)
        print('LOADED: {}'.format(filename))
        shuffle(train_data)
        train = train_data[:-100]
        test = train_data[-100:]
        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,3)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,3)
        test_y = [i[1] for i in test]

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        checkpoint = ModelCheckpoint(filepath="weights/" + MODEL_NAME + ".hdf5", verbose=1, save_best_only=True)
        callbacks_list = [checkpoint]
        model.fit(X, np.array(Y), validation_data=(test_x, np.array(test_y)), callbacks=callbacks_list, 
            verbose=1,  batch_size=32)
    


    

# tensorboard --logdir=foo:C:/path/to/log

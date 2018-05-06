import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from alexnet import alexnet
from mobilenet import MobileNet
import tensorflow as tf
import os
import keras

WIDTH = 320
HEIGHT = 240
LR = 1e-3
EPOCHS = 75
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data.model'.format(LR, 'mobilenet',EPOCHS)
n_btch = 71

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

img_input = keras.layers.Input(shape=(WIDTH, HEIGHT, 3))
model = MobileNet(input_tensor=img_input,classes=4) ##alexnet(WIDTH, HEIGHT, LR, output = 4)

for epoch in range(EPOCHS):    
    for i in range(1,n_btch+1):
        train_data = np.load('data/training_data-{}.npy'.format(i))
        print('LOADED: training_data-{}.npy'.format(i))
        
        train = train_data[:-100]
        test = train_data[-100:]
        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
        test_y = [i[1] for i in test]

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, Y, validation_data=(test_x, test_y), 
            verbose=1,  batch_size=256)

    os.chdir('weights')
    model.save(MODEL_NAME)
    os.chdir('..')
    


    

# tensorboard --logdir=foo:C:/path/to/log

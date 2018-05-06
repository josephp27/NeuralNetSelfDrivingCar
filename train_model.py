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
EPOCHS = 2
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data.model'.format(LR, 'mobilenet',EPOCHS)

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

img_input = keras.layers.Input(shape=(WIDTH, HEIGHT, 3))
model = MobileNet(input_tensor=img_input,classes=4) ##alexnet(WIDTH, HEIGHT, LR, output = 4)

for epoch in range(EPOCHS):
    print('\n================================================ Epoch : {}/{} ================================================'. format(epoch + 1, EPOCHS))    
    for filename in os.listdir(os.getcwd() + '/data/'):
        train_data = np.load('data/' + filename)
        print('LOADED: {}'.format(filename))
        
        train = train_data[:-100]
        test = train_data[-100:]
        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,3)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,3)
        test_y = [i[1] for i in test]

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X, np.array(Y), validation_data=(test_x, np.array(test_y)), 
            verbose=1,  batch_size=32)

    os.chdir('weights')
    model.save(MODEL_NAME)
    os.chdir('..')
    


    

# tensorboard --logdir=foo:C:/path/to/log

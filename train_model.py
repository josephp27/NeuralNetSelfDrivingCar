import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
from alexnet import alexnet

WIDTH = 227
HEIGHT = 227
LR = 1e-3
EPOCHS = 10
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data.model'.format(LR, 'alexnetv2',EPOCHS)
n_btch = 6


model = alexnet(WIDTH, HEIGHT, LR, output = 4 )

for epoch in range(0,EPOCHS):
    for i in range(1,n_btch+1):
        
        train_data = np.load('training_data-{}.npy'.format(i))
        train = train_data[:-50]
        test = train_data[-50:]
        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
        test_y = [i[1] for i in test]

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), 
            snapshot_step=500, show_metric=True,  batch_size=512, run_id=MODEL_NAME)

        #     model.fit(X, Y, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), shuffle=True,
        #           show_metric=True, snapshot_step=200, run_id=MODEL_NAME)
        model.save(MODEL_NAME)



# tensorboard --logdir=foo:C:/path/to/log
import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import os
import h5py

lefts = []
rights = []
forwards = []
backwards = []
no_op = []
num = 0
for filename in os.listdir(os.getcwd() + '/data/'):
    print(filename)
    train_data = np.load('data/' + filename)

    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice == [0, 1, 0, 0]:
            backwards.append([img,choice])

        elif choice == [0, 0, 0 ,0]:
            no_op.append([img, choice])

        elif choice == [0, 0, 1, 0]:
            lefts.append([img,choice])
            
        elif choice == [0, 0, 0 ,1]:
            rights.append([img, choice])

        elif choice == [1, 0, 0, 0]:
            forwards.append([img,choice])
            
        elif choice == [1, 0, 1 ,0]:
            # left_forwards.append([img, choice])
            lefts.append([img,choice])

        elif choice == [1, 0, 0 ,1]:
            # right_forwards.append([img, choice])
            rights.append([img, choice])        

        elif choice == [0, 1, 0 ,1]:
            # backwards_right.append([img, choice])
            backwards.append([img,choice])            

        elif choice == [0, 1, 1, 0]:       	
            # backwards_left.append([img, choice])
            backwards.append([img,choice])

        final_data = forwards + lefts + rights + backwards + no_op
   
        np.savez('data/training_data-merged-{}.npz'.format(num), final_data)

        num += 1


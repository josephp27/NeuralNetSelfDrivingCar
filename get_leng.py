import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import os

lefts = []
left_forwards = []
rights = []
right_forwards = []
forwards = []
backwards = []
backwards_left = []
backwards_right = []
no_op = []

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

print('Lefts {} Rights {} Backwards {} Forwards {} FL {} FR {} BL {} BR {} NOOP {}'.format(len(lefts), 
    len(rights), len(backwards), len(forwards), len(left_forwards), 
    len(right_forwards), len(backwards_left), len(backwards_right), len(no_op) ))

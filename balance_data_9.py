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
            left_forwards.append([img, choice])

        elif choice == [1, 0, 0 ,1]:
            right_forwards.append([img, choice])        

        elif choice == [0, 1, 0 ,1]:
            backwards_right.append([img, choice])

        elif choice == [0, 1, 1, 0]:
            backwards_left.append([img, choice])
        
smallest_class = len(backwards_right)

lefts = lefts[:smallest_class]
left_forwards = left_forwards[:smallest_class]
rights = rights[:smallest_class]
right_forwards = right_forwards[:smallest_class]
forwards = forwards[:smallest_class]
backwards = backwards[:smallest_class]
backwards_left = backwards_left[:smallest_class]
backwards_right = backwards_right[:smallest_class]
no_op = no_op[:smallest_class]

print('Lefts {} Rights {} Backwards {} Forwards {} FL {} FR {} BL {} BR {} NOOP {}'.format(len(lefts), 
    len(rights), len(backwards), len(forwards), len(left_forwards), 
    len(right_forwards), len(backwards_left), len(backwards_right), len(no_op) ))

final_data = lefts + left_forwards + rights + right_forwards + forwards + backwards + backwards_left + backwards_right + no_op

chunks = np.array_split(final_data, 5)
for i in range(len(chunks)):        
    np.save('data/training_data-balanced-{}.npy'.format(i), chunks[i])
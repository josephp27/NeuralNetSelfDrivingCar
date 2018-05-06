import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import os

def num_Batch():
	path, dirs, files = next(os.walk(os.getcwd() + '/data/'))
	return len(files)

print(num_Batch())
for i in range (1,num_Batch() + 1):
    train_data = np.load('data/training_data-{}.npy'.format(i))

    df = pd.DataFrame(train_data)
    # print(df.head())
    # print(Counter(df[1].apply(str)))

    lefts = []
    rights = []
    forwards = []
    backwards = []
    no_op = []

    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice[1] == 1:
            backwards.append([img,choice])
        elif choice[2] == 1:
            lefts.append([img,choice])
        elif choice[3] == 1:
            rights.append([img,choice])
        elif choice[0] == 1:
            forwards.append([img,choice])
        else:
            no_op.append([img,choice])

    smallest_class = min(len(lefts), len(rights), len(backwards), len(forwards))
    
    forwards = forwards[:smallest_class]
    lefts = lefts[:smallest_class]
    rights = rights[:smallest_class]
    backwards = backwards[:smallest_class]
    no_op = no_op[:smallest_class]

    final_data = forwards + lefts + rights + backwards + no_op

    print(len(final_data))
    np.save('data/training_data-{}.npy'.format(i), final_data)

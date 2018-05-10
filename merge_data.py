import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import os

final_data = []
leng = len(os.listdir(os.getcwd() + '/data/')) // 3
processed = 0
for filename in os.listdir(os.getcwd() + '/data/'):
    print(filename)
    train_data = np.load('data/' + filename)

    all_data = []
    for data in train_data:
        img = data[0]
        choice = data[1]

        all_data.append([img,choice])

    final_data += all_data

chunks = np.array_split(final_data, 5)
for i in range(len(chunks)):        
    np.save('data/training_data-{}.npy'.format(i), chunks[i])


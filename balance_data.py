# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle

n_btch = 71
for i in range (1,n_btch+1):
    train_data = np.load('training_data-{}.npy'.format(i))

    df = pd.DataFrame(train_data)
    print(df.head())
    print(Counter(df[1].apply(str)))

    lefts = []
    rights = []
    forwards = []
    backwards = []
    
    shuffle(train_data)

    for data in train_data:
        img = data[0]
        choice = data[1]

        if choice[2] == 1:
            lefts.append([img,choice])
        elif choice[3] == 1:
            rights.append([img,choice])
        elif choice[1] == 1:
            backwards.append([img,choice])
        elif choice[0] == 1:
            forwards.append([img,choice])
        else:
            print('no matches')

    if len(rights) > len(lefts) and len(rights)>len(backwards):
        forwards = forwards[:len(rights)]
    if len(lefts) > len(rights) and len(lefts)>len(backwards):
        forwards = forwards[:len(lefts)]
    if len(backwards) > len(lefts) and len(backwards)>len(rights):
        forwards = forwards[:len(backwards)]
##    forwards = forwards[:len(rights)][:len(lefts)][:len(backwards)]
##    lefts = lefts[:len(forwards)]
##    rights = rights[:len(forwards)]
##    backwards = backwards[:len(forwards)]
    
    final_data = forwards + lefts + rights + backwards
    shuffle(final_data)

    np.save('training_data-{}.npy'.format(i), final_data)

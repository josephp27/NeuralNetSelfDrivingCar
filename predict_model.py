import numpy as np
from win32_screen import grab_screen
import cv2
import time
from sendKeys import PressKey,ReleaseKey, W, A, N, D
from alexnet import alexnet
from getkeys import pressed_keys
import tensorflow as tf

WIDTH = 227
HEIGHT = 227
LR = 1e-3
EPOCHS = 500
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data.model'.format(LR, 'alexnetv2',EPOCHS)
n_btch = 71

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

model = alexnet(WIDTH, HEIGHT, LR, output = 4)
model.load(MODEL_NAME)



def releaseAllKeys():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(N)
    ReleaseKey(D)

def straight():
    releaseAllKeys()
    PressKey(W)

def left():
    releaseAllKeys()
    PressKey(W)
    PressKey(A)

def right():
    releaseAllKeys()
    PressKey(W)
    PressKey(D)

def brake():
    releaseAllKeys()
    PressKey(N)

def brakeTurnLeft():
    releaseAllKeys()
    PressKey(N)
    PressKey(A)

def brakeTurnRight():
    releaseAllKeys()
    PressKey(N)
    PressKey(D)

def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.resize(processed_img, (WIDTH, HEIGHT), interpolation = cv2.INTER_AREA)
    return processed_img

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    while(True):
        
        if not paused:
            screen = grab_screen(region=(0, 30, 1024, 768))
            screen = process_img(screen)

            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
            print(prediction)

            turn_thresh = 0.38
            fwd_thresh = 0.50
            brk_thresh = 0.50
            
            if prediction[2] > turn_thresh:
                left()
            elif prediction[3] > turn_thresh:
                right()
            elif prediction[0] > fwd_thresh:
                straight()
            elif prediction[1] > brk_thresh:
                brake()


        keys = keys = pressed_keys()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                time.sleep(1)
        time.sleep(0.09)

main()     


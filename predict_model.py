import numpy as np
from win32_screen import grab_screen
import cv2
import time
from sendKeys import PressKey,ReleaseKey, straight, left, right, brake, releaseAllKeys, forwardTurnLeft, forwardTurnRight, brakeTurnLeft, brakeTurnRight 
from alexnet import alexnet
from mobilenet import MobileNet
from getkeys import pressed_keys
import tensorflow as tf
import keras
import tensorflow as tf
import os
import pandas as pd
from collections import Counter


WIDTH = 320
HEIGHT = 240
LR = 1e-3
EPOCHS = 75
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data'.format(LR, 'mobilenet',EPOCHS)
n_btch = 15


config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

img_input = keras.layers.Input(shape=(WIDTH, HEIGHT, 3))
model = MobileNet(input_tensor=img_input,classes=4) ##alexnet(WIDTH, HEIGHT, LR, output = 4)
##model.load('weights/' + MODEL_NAME)
model.load_weights('weights/' + MODEL_NAME+ '.hdf5')


def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
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
            #cv2.imshow('window', screen)

            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            prediction = model.predict([screen.reshape(-1,WIDTH, HEIGHT, 3)])[0]
            print(prediction)

##            left_thresh = 0.35
##            right_thresh = 0.35
            
            fwd_thresh = 0.000001
            brk_thresh = 0.001

            turn_thresh = 0.9
            
##            fwd_left_thresh = 0.35
##            fwd_right_thresh = 0.9
##            brk_left_thresh = 0.35
##            brk_right_thresh = 0.35
            
            releaseAllKeys()
            
            
            if prediction[2] > turn_thresh or prediction[3]>turn_thresh:
                if prediction[2]>prediction[3]:
                    left()
                else:
                    right()
            if prediction[1] > brk_thresh and prediction[1]>=prediction[2]:
                brake()
            if prediction[0] > fwd_thresh:
                straight()
##            time.sleep(0.03)


            
##            if prediction[1] > brk_thresh:
##                brake()            
##            if prediction[2] > left_thresh:
##                left()
##            if prediction[3] > right_thresh:
##                right()
##            if prediction[0] > fwd_thresh:
##                straight()

                
##            if prediction[4] > fwd_left_thresh:
##                forwardTurnLeft()
##            if prediction[5] > fwd_right_thresh:
##                forwardTurnRight()
##            if prediction[6] > brk_left_thresh:
##                brakeTurnLeft()
##            if prediction[7] > brk_right_thresh:
##                brakeTurnRight()



        keys = keys = pressed_keys()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                releaseAllKeys()
                time.sleep(1)
                
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
main()     


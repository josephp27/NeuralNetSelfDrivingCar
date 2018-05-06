import numpy as np
from win32_screen import grab_screen
import cv2
import time
from sendKeys import PressKey,ReleaseKey, straight, left, right, brake, releaseAllKeys
from alexnet import alexnet
from getkeys import pressed_keys
import tensorflow as tf

WIDTH = 227
HEIGHT = 227
LR = 1e-3
EPOCHS = 75
MODEL_NAME = 'f1-car-{}-{}-{}-epochs-300K-data.model'.format(LR, 'alexnetv2',EPOCHS)
n_btch = 71

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

model = alexnet(WIDTH, HEIGHT, LR, output = 4)
model.load('weights/' + MODEL_NAME)

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
            #cv2.imshow('window', screen)

            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            prediction = model.predict([screen.reshape(WIDTH, HEIGHT, 1)])[0]
##            print(prediction)

            turn_thresh = 0.09
            fwd_thresh = 0.80
            brk_thresh = 0.002
            releaseAllKeys()
            if prediction[1] > brk_thresh:
                brake()            
            if prediction[2] > turn_thresh or prediction[3] > turn_thresh:
                if prediction[2] > prediction[3]:
                    left()
                else:
                    right()
            if prediction[0] > fwd_thresh:
                straight()



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


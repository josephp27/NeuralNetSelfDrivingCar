import numpy as np
from win32_screen import grab_screen
import cv2
import time
from sendKeys import PressKey,ReleaseKey, W, A, N, D
from alexnet import alexnet
from getkeys import pressed_keys

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


def main():
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    while(True):
        straight()
        time.sleep(1)
        right()
        time.sleep(1)
        left()
        time.sleep(1)


main()



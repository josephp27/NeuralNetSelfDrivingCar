import win32api as wapi
import time

keyList = ['A', 'D', 'W', '(', 'T']


def pressed_keys():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys

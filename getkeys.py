import win32api as wapi
import time

keyList = ["%", '\'', 'A', 'Z', 'T']


def pressed_keys():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys
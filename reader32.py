import numpy as np
from PIL import ImageGrab
import cv2
import time
from getkeys import pressed_keys
from win32_screen import grab_screen
import os


starting_value = 1
file_name = 'training_data-{}.npy'.format(starting_value)

training_data = []

def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    return processed_img

def keys_to_output(keys):
    #[A,Z,L,R] boolean values.
    output = [0, 0, 0, 0]

    if 'Z' in keys:
        output[1] = 1
    if '%' in keys:
        output[2] = 1
    if '\'' in keys:
        output[3] = 1
    if 'A' in keys:
        output[0] = 1
    return output

def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    
    for i in list(range(4))[::-1]:
        print('Starting in: ' + str(i + 1))
        time.sleep(1)


    last_time = time.time()
    paused = False
    while True:
        if not paused:
            screen = grab_screen(region=(0, 30, 1024, 768))
            screen = process_img(screen)

            print('Loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            screen = cv2.resize(screen, (227,227), interpolation = cv2.INTER_AREA)
            cv2.imshow('window', screen)
            #paused=True
            keys = pressed_keys()
            output = keys_to_output(keys)
            print(output)
            training_data.append([screen, output])

            if len(training_data) % 100 == 0:
                print(len(training_data))
                
                if len(training_data) == 500:
                    np.save(file_name,training_data)
                    print('SAVED')
                    training_data = []
                    starting_value += 1
                    file_name = 'training_data-{}.npy'.format(starting_value)


        keys = pressed_keys()

        if 'T' in keys:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
                print(len(training_data))
                np.save(file_name, training_data)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main(file_name, starting_value)


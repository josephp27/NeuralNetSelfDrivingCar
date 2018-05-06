import numpy as np
from PIL import ImageGrab
import cv2
import time
from getkeys import pressed_keys
from win32_screen import grab_screen
import os


starting_value = 1
file_name = 'training_data-{}.npy'.format(starting_value)
os.system('cls')

training_data = []

def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    return processed_img

def keys_to_output(keys):
    #[A,Z,L,R] boolean values.
    output = [0,0,0,0]
    if 'W' in keys:
        output[0] = 1
    if '(' in keys:
        output[1] = 1
    if 'A' in keys:
        output[2] = 1
    if 'D' in keys:
        output[3] = 1
    return output

def main(file_name, starting_value):
    file_name = file_name
    starting_value = starting_value
    training_data = []
    
    for i in list(range(4))[::-1]:
        print('Starting in: ' + str(i + 1), end='\r')
        time.sleep(1)


    last_time = time.time()
    paused = False
    while True:
        if not paused:
            last_time = time.time()
            screen = grab_screen(region=(0, 30, 1024, 798))
            screen = process_img(screen)

            screen = cv2.resize(screen, (320,240), interpolation = cv2.INTER_AREA)
            
            #disable this line for faster FPS!!!!!!!!
            cv2.imshow('window', screen)


            keys = pressed_keys()
            output = keys_to_output(keys)

            training_data.append([screen, output])

            if len(training_data) % 100 == 0:
                if len(training_data) == 1000:
                    np.save(file_name,training_data)
                    os.system('cls')
                    print('SAVED {}'.format(file_name))
                    training_data = []
                    starting_value += 1
                    file_name = 'training_data-{}.npy'.format(starting_value)

            print('{} FPS: {}                            '.format(output, 1.0 / (time.time()-last_time)), end="\r")


        keys = pressed_keys()

        if 'T' in keys:
            if paused:
                paused = False
                print('Unpaused!')
                os.system('cls')
                time.sleep(1)
            else:
                print('\nPausing!', end = "")
                paused = True
                time.sleep(1)
                print(' Length: ' + str(len(training_data)))
                np.save(file_name, training_data)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        

main(file_name, starting_value)


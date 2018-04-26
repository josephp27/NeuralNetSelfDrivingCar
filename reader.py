import numpy as np
from PIL import ImageGrab
import cv2
import time
from sendKeys import PressKey, ReleaseKey, A, Z, L, R

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)
    except:
        pass

def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    #processed_img = cv2.Canny(processed_img, threshold1=225, threshold2=75);
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300);

    processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)
    vertices = np.array([[0,768],[0,350],[256,300],[768,300],[1024,350], [1024,768]])
    processed_img = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]),100, 3)
    draw_lines(processed_img, lines)
    return processed_img

def main():
    last_time = time.time()
    while True:
        screen = np.array(ImageGrab.grab(bbox=(0,40,1024,768)))
        new_screen = process_img(screen)

        print('Loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window', new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()


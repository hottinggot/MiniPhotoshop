import cv2
from math import acos, pi, sqrt
import numpy as np


def compute_hue(b, g, r):
    angle = 0
    if b != g != r:
        angle = 0.5*((r-g)+(r-b)) / sqrt((r-g)*(r-g) + (r-b)*(g-b))

    return acos(angle) if b <= g else (2*pi-acos(angle))


def compute_saturation(b, g, r):
    if b+g+r != 0:
        return 1-3*np.min([b, g, r])/(b+g+r)
    else:
        return 1


def compute_intensity(b, g, r):
    return (b+g+r)/3


def rgb_to_hsi(rgb_image):
    height, width = rgb_image.shape[0], rgb_image.shape[1]

    hsi_image = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            b, g, r = rgb_image[i][j][0]/255, rgb_image[i][j][1]/255, rgb_image[i][j][2]/255

            hsi_image[i][j][0] = compute_intensity(b, g, r)
            hsi_image[i][j][1] = compute_saturation(b, g, r)
            hsi_image[i][j][2] = compute_hue(b, g, r)

    return hsi_image


def negative_func(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height = gray_image.shape[0]
    width = gray_image.shape[1]
    for i in range(0, height - 1):
        for j in range(0, width - 1):
            gray_image[i][j] = 255 - gray_image[i][j]

    return gray_image


def power_law_func(image, gamma):

    pix = list()
    for i in range(0, 255):
        pix.append(pow(i/255.0, gamma)*255)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height = gray_image.shape[0]
    width = gray_image.shape[1]

    for i in range(0, height-1):
        for j in range(0, width-1):
            gray_image[i][j] = pix[gray_image[i][j]]

    return gray_image




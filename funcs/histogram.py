import cv2
import numpy as np


def cal_hist(image):
    height, width = image.shape[0], image.shape[1]
    hist = np.zeros(256)
    for i in range(height):
        for j in range(width):
            hist[image[i][j]] += 1

    return hist


def hist_equalization(image):
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height = image.shape[0]
    width = image.shape[1]

    hist = cal_hist(image)

    s = 0
    all_sum = np.sum(hist)
    sum_hist = np.zeros(256)

    for i in range(hist.shape[0]):
        s += hist[i]
        sum_hist[i] = round(s*255/all_sum)

    for i in range(height):
        for j in range(width):
            image[i][j] = sum_hist[image[i][j]]

    return image



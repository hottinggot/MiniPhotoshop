import cv2
import numpy as np


def cal_hist(image):
    height, width = image.shape[0], image.shape[1]
    hist = np.zeros(256)
    for i in range(height):
        for j in range(width):
            hist[image[i][j]] += 1

    return hist


def hist_normalize(hist, height):
    maxi = np.max(hist)
    hist = hist*height/maxi
    return hist


def draw_one_dim_hist(image):
    hist = cal_hist(image)

    hist_w = 512
    hist_h = 400
    hist_size = 256

    bin_w = hist_w/hist_size

    hist_image = np.zeros((hist_h, hist_w))
    norm_hist = hist_normalize(hist, hist_h)

    for i in range(1, hist_w):
        cv2.line(hist_image, (bin_w*(i-1), round(hist_h-norm_hist[i-1])), (bin_w*i, round(hist_h-norm_hist[i])))

    return hist_image


def hist_equalization(hist):
    s = 0
    all_sum = np.sum(hist)
    sum_hist = np.zeros(256)

    for i in range(hist):
        s += hist[i]
        sum_hist[i] = s / all_sum

    return sum_hist



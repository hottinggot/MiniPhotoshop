import cv2
import numpy as np
from math import exp, pi, sqrt


def mean_filter(image, mask):
    size = mask * 2 + 1
    height, width = image.shape[0], image.shape[1]

    filtered_image = np.zeros((height, width))
    for i in range(mask, height - mask):
        for j in range(mask, width - mask):

            s = 0
            for u in range(i - mask, i - mask + size):
                for v in range(j - mask, j - mask + size):
                    s += image[u][v]

            s /= size * size
            filtered_image[i][j] = s

    return filtered_image


def gaussian_filter(image, mask, sigma):
    size = mask * 2 + 1
    height, width = image.shape[0], image.shape[1]
    gaussian_kernel = np.zeros((size, size))
    sigma = sigma * sigma

    for i in range(size):
        for j in range(size):
            u = i - mask
            v = j - mask
            gaussian_kernel[i][j] = exp(-(u * u + v * v) / (2 * sigma)) / 2 * pi * sigma

    filtered_image = np.zeros((height, width))
    for i in range(mask, height - mask):
        for j in range(mask, width - mask):

            num = 0
            for u in range(i - mask, i - mask + size):
                for v in range(j - mask, j - mask + size):
                    num += gaussian_kernel[u - i + mask][v - j + mask] * image[u][v]

            filtered_image[i][j] = num

    return filtered_image


def median_filter(image, mask):
    size = mask * 2 + 1
    height, width = image.shape[0], image.shape[1]
    median_index = int(size*size/2)

    filtered_image = np.zeros((height, width))
    for i in range(mask, height - mask):
        for j in range(mask, width - mask):

            temp_arr = list()
            for u in range(i - mask, i - mask + size):
                for v in range(j - mask, j - mask + size):
                    temp_arr.append(image[u][v])

            temp_arr.sort()
            filtered_image[i][j] = temp_arr[median_index]

    return filtered_image


def highboost_filter(image, a, filter_type):
    mask = 1
    size = mask * 2 + 1
    height, width = image.shape[0], image.shape[1]
    kernel = np.zeros((3, 3))

    if filter_type == 1:
        a += 4
        kernel = np.array([[0, -1, 0], [-1, a, -1], [0, -1, 0]])
    else:
        a += 8
        kernel = np.array([[-1, -1, -1], [-1, a, -1], [-1, -1, -1]])

    filtered_image = np.zeros((height, width))
    for i in range(mask, height - mask):
        for j in range(mask, width - mask):

            num = 0
            for u in range(i - mask, i - mask + size):
                for v in range(j - mask, j - mask + size):
                    num += image[u][v] * kernel[u-i+mask][v-j+mask]

            filtered_image[i][j] = num

    return filtered_image


def prewitt_filter(image, threshold):

    height, width = image.shape[0], image.shape[1]

    mask_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    mask_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

    filtered_image = np.zeros((height, width))
    for i in range(1, height-1):
        for j in range(1, width-1):
            gx, gy = 0
            for u in range(i-1, i+2):
                for v in range(j-1, j+1):
                    gx += image[u][v]*mask_x[u-i+1][v-j+1]
                    gy += image[u][v]*mask_y[u-i+1][v-j+1]
            if sqrt(gx*gx+gy*gy) > threshold:
                filtered_image[i][j] = 255
            else:
                filtered_image[i][j] = 0

    return filtered_image


def sobel_filter(image, threshold):

    height, width = image.shape[0], image.shape[1]
    mask_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    mask_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    filtered_image = np.zeros((height, width))

    for i in range(1, height-1):
        for j in range(1, width-1):
            gx, gy = 0
            for u in range(i-1, i+2):
                for v in range(j-1, j+1):
                    gx += image[u][v]*mask_x[u-i+1][v-j+1]
                    gy += image[u][v]*mask_y[u-i+1][v-j+1]

            if sqrt(gx * gx + gy * gy) > threshold:
                filtered_image[i][j] = 255
            else:
                filtered_image[i][j] = 0

    return filtered_image


def LoG_filter(image, mask, sigma):
    size = mask*2+1
    height, width = image.shape[0], image.shape[1]
    sigma = sigma*sigma
    log_kernel = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            u = i-mask
            v = j-mask
            log_kernel[i][j] = -(((u*u + v*v)/sigma - 2)*exp(-(u*u+v*v)/(2*sigma))) / 2*pi*sigma*sigma

    temp_image = np.zeros((height, width))
    for i in range(mask, height-mask):
        for j in range(mask, width-mask):
            num = 0
            for u in range(i-mask, i-mask+size):
                for v in range(j-mask, j-mask+size):
                    num += image[u][v]*log_kernel[u-i+mask][v-j+mask]

            if num > 0:
                temp_image[i][j] = 1
            else:
                temp_image[i][j] = -1

    filtered_image = np.zeros((height, width))
    for i in range(1, height):
        for j in range(1, width):
            if (temp_image[i][j] * temp_image[i-1][j] > 0) and (temp_image[i][j]*temp_image[i][j-1] > 0):
                filtered_image[i][j] = 0
            else:
                filtered_image[i][j] = 255

    return filtered_image


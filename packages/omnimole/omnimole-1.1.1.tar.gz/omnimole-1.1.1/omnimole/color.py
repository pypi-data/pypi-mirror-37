import cv2
import numpy as np


def image_stats(image):
    """ Splits an image into channels, and computes mean and std on each channel.
    :param image: an image to be split
    :return stats with the following format:
    (first.mean, first.std, second.mean, second.std, third.mean, third.std) """
    l, a, b = cv2.split(image)

    l_noblack = []
    a_noblack = []
    b_noblack = []

    for i, row in enumerate(l):
        for j, pixel in enumerate(row):
            if l[i][j] != 0:
                l_noblack.append(l[i][j])
                a_noblack.append(a[i][j])
                b_noblack.append(b[i][j])

    l_noblack = np.array(l_noblack)
    a_noblack = np.array(a_noblack)
    b_noblack = np.array(b_noblack)
    return l_noblack.mean(), l_noblack.std(), a_noblack.mean(), a_noblack.std(), b_noblack.mean(), b_noblack.std()


def clahe_equalize(image):
    """ Takes a color image, performs CLAHE (Contrast Limited Adaptive Histogram Equalization).
    :param image: image in BGR colorspace
    :return equalized image in BGR colorspace """

    # read in image and convert to HSV
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # split into channels
    h, s, v = cv2.split(image)

    # create CLAHE object
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    equ_v = clahe.apply(v)

    # merge and convert back to BGR
    equ_image = cv2.merge((h, s, equ_v))
    equ_image = cv2.cvtColor(equ_image, cv2.COLOR_HSV2BGR)

    return equ_image


def transfer_color(source, target):
    """Takes the colormap of source image and maps it on to target image.
    For normalizing color between two different data.
    :param source: The source image
    :param target: The target image
    :return target image with source image color"""

    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # color statistics for source and target image
    l_mean_src, l_std_src, a_mean_src, a_std_src, b_mean_src, b_std_src = image_stats(source)
    l_mean_tar, l_std_tar, a_mean_tar, a_std_tar, b_mean_tar, b_std_tar = image_stats(target)

    # subtract means from target image
    l, a, b = cv2.split(target)
    l -= l_mean_tar
    a -= a_mean_tar
    b -= b_mean_tar

    # scale by the standard deviation
    l = (l_std_tar / l_std_src) * l
    a = (a_std_tar / a_std_src) * a
    b = (b_std_tar / b_std_src) * b

    # add in the source mean
    l += l_mean_src
    a += a_mean_src
    b += b_mean_src

    # clip the pixel intensities to [0, 255] if they fall outside this range
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # merge channels together and convert back to RGB color space
    # make sure to use 8-bit unsigned int
    transfer = cv2.merge([l, a, b])
    transfer_image = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)

    return transfer_image

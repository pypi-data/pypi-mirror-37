import cv2
import imutils
from math import floor, ceil


def resize(image, width=500, height=500):
    """ Resizes and image, keeping the original aspect ratio
    :param image: the image to resize
    :param width: the max width of the new image
    :param height: the max height of the new image
    :return: the image resized to a max of 500x500 """
    image = imutils.resize(image, width=width, height=height)
    return image


def match_size(image_1, image_2, width=500, height=500):
    """ Resizes both images to the same size, padding when necessary
    :param image_1: the first image
    :param image_2: the second image
    :param width: the max width of the new images
    :param height: the max height of the new images
    :return: both images, resized to the same size """
    # Resize the data to a more manageable size
    image_1 = imutils.resize(image_1, width=width, height=height)
    image_2 = imutils.resize(image_2, width=width, height=height)

    # Pad the data to have matching dimensions
    height_1, width_1 = image_1.shape[:2]
    height_2, width_2 = image_2.shape[:2]
    vertical = height_1 - height_2
    horizontal = width_1 - width_2

    top = floor(vertical / 2)
    bottom = ceil(vertical / 2)
    left = floor(horizontal / 2)
    right = ceil(horizontal / 2)
    if vertical < 0:
        image_1 = cv2.copyMakeBorder(image_1, borderType=cv2.BORDER_CONSTANT,
                                     top=abs(top), bottom=abs(bottom), left=0, right=0)
    else:
        image_2 = cv2.copyMakeBorder(image_2, borderType=cv2.BORDER_CONSTANT,
                                     top=top, bottom=bottom, left=0, right=0)
    if horizontal < 0:
        image_1 = cv2.copyMakeBorder(image_1, borderType=cv2.BORDER_CONSTANT,
                                     top=0, bottom=0, left=abs(left), right=abs(right))
    else:
        image_2 = cv2.copyMakeBorder(image_2, borderType=cv2.BORDER_CONSTANT,
                                     top=0, bottom=0, left=left, right=right)

    return image_1, image_2

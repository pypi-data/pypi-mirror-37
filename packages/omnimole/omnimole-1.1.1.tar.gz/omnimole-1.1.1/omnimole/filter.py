import cv2
import numpy as np


def enhance_edges(image, action='edge_enhance', kernel=None):
    """ Applies an edge filter to an image, accentuating edges
    :param image: the image to be filtered
    :param action: the desired action (sharpen, exc_sharpen, edge_enhance)
    :param kernel: an override kernel to apply to the image
    :return the image with edges enhanced """
    if not kernel:
        if action == 'sharpen':
            kernel = np.array([[-1, -1, -1],
                               [-1, +9, -1],
                               [-1, -1, -1]])
        elif action == 'exc_sharpen':
            kernel = np.array([[+1, +1, +1],
                               [+1, -7, +1],
                               [+1, +1, +1]])
        elif action == 'edge_enhance':
            kernel = np.array([[-1, -1, -1, -1, -1],
                               [-1, +2, +2, +2, -1],
                               [-1, +2, +8, +2, -1],
                               [-1, +2, +2, +2, -1],
                               [-1, -1, -1, -1, -1]]) / 8.0
        else:
            raise ValueError(action + ' not implemented')

    edge_image = cv2.filter2D(image, -1, kernel=kernel)
    return edge_image

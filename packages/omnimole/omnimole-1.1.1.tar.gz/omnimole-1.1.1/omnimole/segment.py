import cv2
import maxflow
import numpy as np
from math import exp, pow


# Skin pixel values for YCrCb
# Y = 0-255
# Cr = 130-180
# Cb = 75-135

def grabcut_segment(image, rect=None):
    """ Segments the image, assuming that the outer border is representative of the
    background (possible rect would be (25, 0, cols - 50, rows))
    :param image: the original image
    :param rect: the bounding box which contains the foreground, or None for custom
    :return: the image with only the skin """
    rows, cols = image.shape[:2]

    mask_image = None
    mask = np.zeros((rows, cols), np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)

    if rect:
        cv2.grabCut(image, mask, rect, bg_model, fg_model, 5, cv2.GC_INIT_WITH_RECT)
    else:
        r = rows / 2.
        c = cols / 2.
        d = r if r > c else c

        for i in range(rows):
            for j in range(cols):
                dist = np.sqrt((i - r) ** 2 + (j - c) ** 2)
                if dist < (1. / 3.) * d:
                    mask[i, j] = 1
                elif dist < (2. / 3.) * d:
                    mask[i, j] = 3
                elif dist < d:
                    mask[i, j] = 2

        mask_image = mask * 80
        cv2.grabCut(image, mask, None, bg_model, fg_model, 5, cv2.GC_INIT_WITH_MASK)

    mask = np.where((mask == 0) | (mask == 2), 0, 1).astype(np.uint8)
    grabcut = image * mask[:, :, np.newaxis]

    return grabcut, mask_image


def mrf_segment(image, cost_image, mu_1=130, mu_2=155, mu_3=105,
                sigma_1=100, sigma_2=25, sigma_3=30, pairwise=100):
    """ Segments an image as a Markov random field
    :param image: the original image
    :param cost_image: image on which to base the costs
    :param mu_1: mean of the first channel
    :param mu_2: mean of the second channel
    :param mu_3: mean of the third channel
    :param sigma_1: std of the first channel
    :param sigma_2: std of the second channel
    :param sigma_3: std of the third channel
    :param pairwise: the pairwise cost for the MRF
    :return: the segmented image """
    costs = [[gaussian_kernel_3(pixel, mu_1, sigma_1, mu_2, sigma_2, mu_3, sigma_3)
              for pixel in row] for row in cost_image]
    costs = np.array(costs)

    # Create graph
    g = maxflow.Graph[float]()
    nodes = g.add_grid_nodes(image.shape[:2])
    g.add_grid_edges(nodes, pairwise)
    g.add_grid_tedges(nodes, 100 - costs, costs)

    # Compute maxflow
    g.maxflow()

    # Mask the original image
    segments = g.get_grid_segments(nodes)
    labels = np.array(segments, dtype=np.uint8)
    mrf = cv2.bitwise_and(image, image, mask=labels)

    return mrf


def threshold_segment(image, space='ycrcb'):
    """ Takes an image applies a mask in the YCrCb colorspace to segment only skin.
    SOURCES:
    - Face Segmentation Using Skin-Color Map in Videophone Applications by Chai and Ngan
    - Skin Detection: A Step-by-Step Example Using Python and OpenCV by Adrian Rosebrock
    :param image: the image to segment
    :param space: the color space in which to segment the image
    :param lower: the lower threshold for skin in the color space
    :param upper: the higher threshold for skin in the color space
    :return filtered skin image in BGR color space and black and white mask """
    m, n = image.shape[:2]
    skin_mask = np.zeros((m, n), dtype=np.uint8)

    if space == 'hsv':
        lower = np.array([0, 45, 80], dtype=np.uint8)
        upper = np.array([20, 255, 255], dtype=np.uint8)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        return threshold_skin(image, hsv, lower, upper)

    elif space == 'rgb':
        for i in range(0, m):
            for j in range(0, n):
                r, g, b = image[i][j]
                if r > 95 and g > 40 and b > 20 and r > g and r > b \
                        and max(r, g, b) - min(r, g, b) > 15 and abs(r - g) > 15:
                    skin_mask[i][j] = 255
        return mask_skin(image, skin_mask)

    elif space == 'ycrcb':
        lower = np.array([0, 130, 80], dtype=np.uint8)
        upper = np.array([255, 180, 130], dtype=np.uint8)
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        return threshold_skin(image, ycrcb, lower, upper)

    elif space == 'yuv':
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        for i in range(0, m):
            for j in range(0, n):
                r, g, b = image[i][j]
                y, u, v = converted[i][j]

                if 80 < u < 130 and 136 < v < 200 \
                        and r > 80 and g > 30 and b > 15 and abs(r - g) > 15:
                    skin_mask[i][j] = 255
        return mask_skin(image, skin_mask)

    else:
        raise ValueError(space + ' not implemented')


# -------------------------------------------------------- #
# -------------------- Helper Methods -------------------- #
# -------------------------------------------------------- #
def gaussian_kernel_2(pixel, mu_1, sigma_1, mu_2, sigma_2):
    d = exp(-(
        pow(mu_1 - pixel[0], 2) / (2 * pow(sigma_1, 2)) +
        pow(mu_2 - pixel[2], 2) / (2 * pow(sigma_2, 2))))
    return d * 100


def gaussian_kernel_3(pixel, mu_1, sigma_1, mu_2, sigma_2, mu_3, sigma_3):
    n = 1  # No normalization
    # n = 1 / (pow(2 * pi, 3 / 2) * y_sigma * cr_sigma * cb_sigma)

    d = exp(-(
        pow(mu_1 - pixel[0], 2) / (2 * pow(sigma_1, 2)) +
        pow(mu_2 - pixel[1], 2) / (2 * pow(sigma_2, 2)) +
        pow(mu_3 - pixel[2], 2) / (2 * pow(sigma_3, 2))))
    return n * d * 100


def threshold_moles(image, method='adaptive'):
    """ Performs adaptive or otsu thresholding on an image
    :param image: the original image
    :param method: 'adaptive' or 'otsu' thresholding
    :return: the thresholded image """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if method == 'adaptive':
        thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 50, 50)
    elif method == 'otsu':
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        raise ValueError(method + ' not implemented')

    image = cv2.bitwise_and(image, image, mask=thresh)
    return image


def threshold_skin(image, converted, lower, upper):
    skin_mask = cv2.inRange(converted, lower, upper)
    return mask_skin(image, skin_mask)


def mask_skin(image, skin_mask):
    # Apply erosions and dilations to mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skin_mask = cv2.erode(skin_mask, kernel, iterations=2)
    skin_mask = cv2.dilate(skin_mask, kernel, iterations=2)

    # Blur and apply mask
    skin_mask = cv2.GaussianBlur(skin_mask, (3, 3), 0)
    skin_image = cv2.bitwise_and(image, image, mask=skin_mask)

    return skin_image, skin_mask


def skinmask_overlay(base_image, overlay_image, alpha=0.5):
    """ Takes two data, takes the skinmask of the first image and overlays it on the
    seconds image (for camera) returns the overlayed image
    :param base_image: the base image
    :param overlay_image: the image to overlay
    :param alpha: the amount of transparency
    :return the overlayed image on the base image """
    skin_base, _ = threshold_segment(base_image)
    cv2.addWeighted(skin_base, alpha, overlay_image, 1 - alpha, 0, overlay_image)

    return overlay_image

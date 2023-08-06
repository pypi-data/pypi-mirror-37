import cv2
import numpy as np


def ecc_alignment(image_1, image_2, iterations=1000, term_eps=1e-5):
    """ Takes two data, performs a perspective transformation to foreground orientation
    Returns second image as aligned to the first
    :param image_1: the image to which the second image should be aligned
    :param image_2: the image to align to the first image
    :param iterations: number of iterations
    :param term_eps: threshold of increment in correlation coefficient between iterations
    :return the aligned second image """
    rows, cols = image_1.shape[:2]

    image_1_gray = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
    image_2_gray = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)

    warp_mode = cv2.MOTION_HOMOGRAPHY
    warp_matrix = np.eye(3, 3, dtype=np.float32)

    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, iterations, term_eps)

    # Run the ECC algorithm. The results are stored in warp_matrix.
    cc, warp_matrix = cv2.findTransformECC(image_1_gray, image_2_gray, warp_matrix, warp_mode, criteria)

    # Warps image based on homography matrix from ECC algorithm
    image_2_aligned = cv2.warpPerspective(image_2, warp_matrix, (cols, rows),
                                          flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

    return image_2_aligned


def correspondence_warp(image_1, points_1, image_2, points_2):
    """ Warps the second image into the first image, based on the correspondences
    :param image_1: the first image
    :param points_1: ordered coordinates of the landmarks in the first image
    :param image_2: the second image
    :param points_2: ordered coordinates of the landmarks in the second image
    :return: the second image warped into the first image """
    for (x, y) in points_1:
        cv2.circle(image_1, (x, y), 3, 0, -1)
    for (x, y) in points_2:
        cv2.circle(image_2, (x, y), 3, 0, -1)

    # mat_warp = cv2.getPerspectiveTransform(points_2, points_1)
    mat_warp, status = cv2.findHomography(points_2, points_1)
    warped = cv2.warpPerspective(image_2, mat_warp, (image_1.shape[1], image_1.shape[0]))

    return warped

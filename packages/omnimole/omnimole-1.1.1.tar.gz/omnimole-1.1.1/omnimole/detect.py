import cv2
import numpy as np
from sklearn.decomposition import PCA
from .segment import threshold_segment


def detect_moles(image, matching, min_area=10, max_area=100, pca_comp=0):
    """ Draws a circle around all moles in the image
    :param image: an image with moles to detect
    :param matching:
    :param min_area:
    :param max_area:
    :param pca_comp:
    :return the image with keypoints circled """
    params = cv2.SimpleBlobDetector_Params()

    # Filters
    params.filterByArea = True
    params.minArea = min_area
    params.maxArea = max_area
    params.filterByCircularity = False
    params.minCircularity = 0.1
    params.filterByConvexity = False
    params.minConvexity = 0.5
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    # Detect keypoints
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(image)

    # Compute descriptors
    descriptors = []
    comps = None
    if pca_comp > 0:
        orb = cv2.ORB_create()
        keypoints, descriptors = orb.compute(image, keypoints)

        pca = PCA(n_components=pca_comp)
        comps = pca.fit_transform(descriptors)

    # Use position as part of the descriptor
    if matching == 'NN':
        pad = 30 - pca_comp
        reduced = np.zeros((len(keypoints), pad))
        if comps:
            reduced = np.hstack((comps, reduced))

        descriptors = [np.array(keypoint.pt) for keypoint in keypoints]
        descriptors = np.hstack((descriptors, reduced)).astype(np.float32)

    return image, keypoints, descriptors


def detect_contours(image):
    """ Finds contours around skin.
    :param image: an image
    :return contour-overlay image and contour """
    _, skin_mask = threshold_segment(image)

    # Do contour detection on skin mask
    _, contours, hierarchy = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    skin_contours = []
    # Draw the contour on the source image
    for i, c in enumerate(contours):
        # grab only contours of a certain size
        area = cv2.contourArea(c)
        if area > 6000:
            skin_contours.append(c)
            # specify precision as 1/1000 of total perimeter
            # peri = cv2.arcLength(c, True)
            # contours[i] = cv2.approxPolyDP(c, 0.001 * peri, True)
            # overlay the contour on the original image
            cv2.drawContours(image, contours, i, (0, 255, 0), 3)

    return image, skin_contours


def contour_overlay(base_image, overlay_image):
    """ Finds contours of base image and overlays them on the target image
    to help align data (for camera), returns overlayed image
    :param base_image: the base image
    :param overlay_image: the image on which to overlay contours
    :return the target image with the contours from the base image overlayed"""
    _, contours = detect_contours(base_image)

    for i, contour in enumerate(contours):
        cv2.drawContours(overlay_image, contours, i, (0, 0, 255), 3)

    return overlay_image

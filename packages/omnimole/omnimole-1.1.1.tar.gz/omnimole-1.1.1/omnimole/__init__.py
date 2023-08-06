import cv2
from skimage import io

from .color import clahe_equalize, transfer_color
from .filter import enhance_edges
from .preprocess import resize, match_size
from .register import ecc_alignment
from .segment import grabcut_segment
from .detect import detect_moles


def process(image_1_path, image_2_path=None, match='BF', matching='NN'):
    # -------------------------------------------------------- #
    # -------------------- Image Pipeline -------------------- #
    # -------------------------------------------------------- #
    image_2 = None
    match_image = None

    # First image arrives
    image_1 = cv2.cvtColor(io.imread(image_1_path), cv2.COLOR_BGR2RGB)
    image_1 = resize(image_1)
    he_image_1 = clahe_equalize(image_1)

    # cv2.RECURS_FILTER
    # cv2.NORMCONV_FILTER
    image_1 = cv2.edgePreservingFilter(he_image_1, sigma_s=15, sigma_r=0.15)
    image_1 = enhance_edges(image_1)
    image_1, _ = grabcut_segment(image_1)

    if image_2_path:
        image_2 = cv2.cvtColor(io.imread(image_2_path), cv2.COLOR_BGR2RGB)
        image_1, image_2 = match_size(image_1, image_2)
        he_image_1, _ = match_size(he_image_1, image_2)

        # Second image arrives
        image_2 = clahe_equalize(image_2)
        image_2 = transfer_color(he_image_1, image_2)
        image_2 = cv2.edgePreservingFilter(image_2, sigma_s=15, sigma_r=0.15)
        image_2 = enhance_edges(image_2)
        image_2, _ = grabcut_segment(image_2)
        image_2 = ecc_alignment(image_1, image_2)

        # Detect the moles
        image_1, keypoints_1, des_1 = detect_moles(image_1, matching)
        image_2, keypoints_2, des_2 = detect_moles(image_2, matching)

        # Match desciptors
        if match == 'BF':
            if matching == 'NN':
                matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
            else:
                matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        else:
            if matching == 'NN':
                index_params = dict(algorithm=0, trees=5)
            else:
                index_params = dict(algorithm=6,
                                    table_number=12, key_size=20, multi_probe_level=2)
            search_params = dict(checks=50)  # or pass empty dictionary
            matcher = cv2.FlannBasedMatcher(index_params, search_params)

        # Find matches
        matches = matcher.match(des_1, des_2)
        matches = sorted(matches, key=lambda x: x.distance)
        match_image = cv2.drawMatches(image_1, keypoints_1, image_2, keypoints_2, matches, None)

    return image_1, image_2, match_image

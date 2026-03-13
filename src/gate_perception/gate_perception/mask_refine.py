import cv2
import numpy as np

def refine_mask(mask):

    kernel = np.ones((5,5),np.uint8)

    # remove noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # fill gaps
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # smooth
    mask = cv2.GaussianBlur(mask,(5,5),0)

    return mask
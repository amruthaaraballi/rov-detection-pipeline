import cv2
import numpy as np
from sklearn.linear_model import RANSACRegressor

def hough_lines(mask):

    edges = cv2.Canny(mask,50,150)

    lines = cv2.HoughLinesP(
        edges,
        1,
        np.pi/180,
        threshold=50,
        minLineLength=50,
        maxLineGap=10
    )

    return lines


def least_squares(points):

    x = points[:,0]
    y = points[:,1]

    A = np.vstack([x,np.ones(len(x))]).T
    m,c = np.linalg.lstsq(A,y,rcond=None)[0]

    return m,c


def ransac_line(points):

    x = points[:,0].reshape(-1,1)
    y = points[:,1]

    model = RANSACRegressor()
    model.fit(x,y)

    m = model.estimator_.coef_[0]
    c = model.estimator_.intercept_

    return m,c
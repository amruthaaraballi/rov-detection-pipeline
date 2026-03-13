import numpy as np
from sklearn.linear_model import LinearRegression

def fit_plane(points):

    X = points[:, :2]
    Z = points[:, 2]

    model = LinearRegression()
    model.fit(X, Z)

    a = model.coef_[0]
    b = model.coef_[1]
    c = -1
    d = model.intercept_

    return a,b,c,d
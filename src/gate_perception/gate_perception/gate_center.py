import numpy as np

def compute_centroid(points):

    centroid = np.mean(points, axis=0)

    return centroid
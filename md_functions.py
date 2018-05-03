import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import pdist, squareform

def find_largest_dist(at_pos):

    D = pdist(np.asarray(at_pos))
    D = squareform(D)
    return np.nanmax(D)

def find_largest_dist_con(at_pos):
    hull = ConvexHull(at_pos)
    D = pdist(np.asarray(hull.points))
    D = squareform(D)
    return np.nanmax(D)


def insert_line(line,key,dat):
    for i, ent in enumerate(dat):
        if  key in ent:
            dat[i] = line
            break
    return dat




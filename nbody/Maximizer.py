from n_body_lib import maximize_function
from n_body_lib import np
from n_body_lib import monotonic
from n_body_lib import v
from n_body_lib import scal

# values = [2, 45, 57, 83, 4, 1]

def maximize_dist(points, dist: callable):
    distances = []
    for i in points:
        for j in points:
            distances.append(dist(i, j))
    return max(distances)
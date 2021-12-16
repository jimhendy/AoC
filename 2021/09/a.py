import os
import numpy as np
from tools.point import Point2D


def run(inputs):
    total_risk = 0
    heightmap = np.array([list(l) for l in inputs.split(os.linesep)]).astype(int)
    for x in range(heightmap.shape[1]):
        for y in range(heightmap.shape[0]):
            h = heightmap[y, x]
            p = Point2D(x, y)
            is_lowest = True
            for pp in p.nb4(grid_size=heightmap.shape):

                if heightmap[pp.y, pp.x] <= h:
                    is_lowest = False
                    break

            if is_lowest:
                total_risk += h + 1

    return total_risk

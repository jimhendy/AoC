import os
import numpy as np
from tools.point import Point2D


def run(inputs):

    heightmap = np.array([list(l) for l in inputs.split(os.linesep)]).astype(int)
    basin_sizes = []
    for x in range(heightmap.shape[1]):
        for y in range(heightmap.shape[0]):
            h = heightmap[y, x]
            low_point = Point2D(x, y)
            is_lowest = True
            for pp in low_point.nb4():

                if pp.x[0] < 0 or pp.x[0] == heightmap.shape[1]:
                    continue
                if pp.x[1] < 0 or pp.x[1] == heightmap.shape[0]:
                    continue

                if heightmap[pp.x[1], pp.x[0]] <= h:
                    is_lowest = False
                    break

            if is_lowest:
                points_in_basin = set([low_point])
                points_to_analyse = [low_point]
                seen = set([low_point])
                while len(points_to_analyse):
                    p = points_to_analyse.pop()

                    for pp in p.nb4():

                        if pp in seen:
                            continue
                        if pp.x[0] < 0 or pp.x[0] == heightmap.shape[1]:
                            continue
                        if pp.x[1] < 0 or pp.x[1] == heightmap.shape[0]:
                            continue

                        if heightmap[pp.x[1], pp.x[0]] == 9:
                            continue

                        seen.add(pp)
                        points_in_basin.add(pp)
                        points_to_analyse.append(pp)

                basin_sizes.append(len(points_in_basin))

    return np.prod(sorted(basin_sizes)[-3:])
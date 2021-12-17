import numpy as np


def run(inputs):
    x_target = list(map(int, inputs.split("x=")[1].split(",")[0].split("..")))
    y_target = list(map(int, inputs.split("y=")[1].split("..")))

    xs = np.arange(x_target[1] + 1)
    ys = np.arange(y_target[0], max(np.abs(y_target)) + 1)

    velocities = np.array(np.meshgrid(xs, ys)).T.reshape(-1, 2)

    pos = np.full(velocities.shape, 0)
    below_target = np.zeros(pos.shape[0]).astype(bool)
    hit_target = np.zeros_like(below_target).astype(bool)

    while False in below_target:
        pos += velocities

        velocities[velocities[:, 0] > 0, 0] -= 1
        velocities[velocities[:, 0] < 0, 0] += 1
        velocities[:, 1] -= 1

        below_target[pos[:, 1] < y_target[1]] = True

        in_target = np.logical_and(
            np.logical_and(x_target[0] <= pos[:, 0], pos[:, 0] <= x_target[1]),
            np.logical_and(y_target[0] <= pos[:, 1], pos[:, 1] <= y_target[1]),
        )
        hit_target[in_target] = True

    return hit_target.sum()
import numpy as np
from loguru import logger


def are_points_collinear(points):
    # Use the first point as the reference
    ref_point = points[0]

    # Compute direction vectors from the reference point
    direction_vectors = points[1:] - ref_point

    # Check if we have only one direction vector (meaning only two points)
    if len(direction_vectors) == 1:
        return True  # Two points are always collinear

    # Compute cross products of all direction vectors with the first direction vector
    cross_products = np.cross(direction_vectors[0], direction_vectors[1:])

    # Check if all cross products are zero (within a tolerance for floating-point precision)
    return np.all(np.isclose(cross_products, 0))


def run(inputs: str) -> int:
    particles = []
    velocities = []
    for line in inputs.splitlines():
        p, v = line.split("@")
        particles.append(list(map(int, p.split(","))))
        velocities.append(list(map(int, v.split(","))))

    particles = np.array(particles)
    velocities = np.array(velocities)

    for t in range(100):
        logger.debug(f"Time: {t}")
        if are_points_collinear(particles):
            logger.debug(f"Particles are collinear at time {t}")
            return t
        logger.info("Particles are not collinear")
        particles += velocities


np.array(
    [list(map(int, line.split(","))) for line in data.replace("@", ",").splitlines()]
)

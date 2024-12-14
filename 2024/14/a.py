from functools import reduce

STEPS = 100
WIDTH = 101
HEIGHT = 103


def run(inputs: str) -> int:
    quadrant_counts = [0, 0, 0, 0]
    for line in inputs.splitlines():
        pos, vel = line.split()
        px, py = list(map(int, pos.removeprefix("p=").split(",")))
        vx, vy = list(map(int, vel.removeprefix("v=").split(",")))

        for _ in range(STEPS):
            px += vx
            py += vy
            if px < 0:
                px += WIDTH
            elif px >= WIDTH:
                px -= WIDTH
            if py < 0:
                py += HEIGHT
            elif py >= HEIGHT:
                py -= HEIGHT

        if px == (WIDTH - 1) / 2 or py == (HEIGHT - 1) / 2:
            continue

        i = 0 if px < WIDTH / 2 else 2
        i += 0 if py < HEIGHT / 2 else 1
        quadrant_counts[i] += 1

    return reduce(lambda x, y: x * y, quadrant_counts)

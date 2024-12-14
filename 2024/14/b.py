from pathlib import Path

import matplotlib.pyplot as plt
import skimage.measure

WIDTH = 101
HEIGHT = 103
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
ENTROPY_THRESHOLD = 0.2675
FIND_MODE = False


def run(inputs: str) -> int:
    positions = []
    velocities = []

    for line in inputs.splitlines():
        pos, vel = line.split()
        px, py = list(map(int, pos.removeprefix("p=").split(",")))
        vx, vy = list(map(int, vel.removeprefix("v=").split(",")))

        positions.append((px, py))
        velocities.append((vx, vy))

    step = 0
    entropy = {}
    while True:
        if FIND_MODE:
            # Add the entropy of the current positions to the entropy dictionary
            entropy[step] = skimage.measure.shannon_entropy(
                [
                    [1 if (px, py) in positions else 0 for px in range(WIDTH)]
                    for py in range(HEIGHT)
                ],
            )

            if entropy[step] < ENTROPY_THRESHOLD:
                # Print a heatmap of the positions and present to the user
                # The title should be the number of steps taken
                plt.imshow(
                    [
                        [1 if (px, py) in positions else 0 for px in range(WIDTH)]
                        for py in range(HEIGHT)
                    ],
                )
                plt.title(f"Steps: {step}")
                plt.savefig(OUTPUT_DIR / f"step_{step}.png")
                plt.clf()

            if step % 100 == 0:
                print(f"Step: {step}")
                # Plot the entropy dictionary
                plt.plot(entropy.keys(), entropy.values())
                plt.xlabel("Step")
                plt.ylabel("Entropy")
                plt.title("Entropy over time")
                plt.savefig(OUTPUT_DIR / "entropy.png")
                plt.clf()

        elif step == 7055:
            plt.imshow(
                [
                    [1 if (px, py) in positions else 0 for px in range(WIDTH)]
                    for py in range(HEIGHT)
                ],
            )
            plt.title(f"Steps: {step}")
            plt.savefig(OUTPUT_DIR / f"step_{step}.png")
            plt.show()
            break

        for i, (px, py) in enumerate(positions):
            vx, vy = velocities[i]
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
            positions[i] = (px, py)

        step += 1

    return step

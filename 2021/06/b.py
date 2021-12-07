from collections import Counter, defaultdict


def run(inputs):
    fish = Counter(map(int, inputs.split(",")))

    for _ in range(256):
        new_fish = defaultdict(int)
        for k, v in fish.items():
            if k == 0:
                new_fish[6] += v
                new_fish[8] = v
            else:
                new_fish[k - 1] += v
        fish = new_fish

    return sum(fish.values())
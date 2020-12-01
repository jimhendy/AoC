import os


def run(inputs):
    nums = list(map(int, inputs.split(os.linesep)))
    for i, n_i in enumerate(nums[:-1]):
        for n_j in nums[i + 1 :]:
            if n_i + n_j == 2020:
                return n_i * n_j

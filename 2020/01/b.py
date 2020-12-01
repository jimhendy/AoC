import os


def run(inputs):
    nums = list(map(int, inputs.split(os.linesep)))
    for i, n_i in enumerate(nums[:-2]):
        for j, n_j in enumerate(nums[i:-1]):
            if n_i + n_j >= 2020:
                continue
            for n_k in nums[j + 1 :]:
                if n_i + n_j + n_k == 2020:
                    return n_i * n_j * n_k

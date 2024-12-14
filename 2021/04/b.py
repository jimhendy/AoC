import os
from itertools import chain

import numpy as np


class Board:
    def __init__(self, nums: list[list[int]]) -> None:
        self.nums = np.array(nums)
        self.size = self.nums.shape[0]
        self.rows = [set(i) for i in self.nums]
        self.cols = [set(i) for i in self.nums.T]
        self.total = self.nums.sum()
        self.all_nums = set(self.nums.flatten().tolist())

    def check(self, marked: set):
        for n in chain(self.rows, self.cols):
            if len(marked.intersection(n)) == self.size:
                return self.total - sum(marked.intersection(self.all_nums))
        return None


def run(inputs):
    inputs = inputs.split(os.linesep)
    called_nums = list(map(int, inputs[0].split(",")))
    nums = []
    boards = []
    complete_boards = set()
    for l in inputs[2:]:
        if not l:
            boards.append(Board(nums))
            nums = []
        else:
            nums.append(list(map(int, l.split())))
    if len(nums):
        boards.append(Board(nums))

    for i, n in enumerate(called_nums):
        called_set = set(called_nums[: i + 1])
        for b, board in enumerate(boards):
            if b in complete_boards:
                continue
            result = board.check(called_set)
            if result is not None:
                if len(complete_boards) == len(boards) - 1:
                    return result * n
                complete_boards.add(b)
    return None

import os
import re
from functools import lru_cache

import a_star
import numpy as np

WALL_CHAR = "#"
SPACE_CHAR = "."


class Maze:
    def __init__(self, maze_as_str) -> None:
        self.maze_as_str = maze_as_str
        self.maze = np.array(
            [list(i) for i in self.maze_as_str.split(os.linesep)],
        )
        self.steps_between_store = {}

    @lru_cache(maxsize=1)
    def number_locations(self):
        return {
            int(n): np.array((x, y))
            for x, row in enumerate(self.maze)
            for y, n in enumerate(row)
            if Maze.char_is_number(n)
        }

    @staticmethod
    @lru_cache(maxsize=48)
    def char_is_number(char):
        return re.search(r"^-?\d+$", char)

    @staticmethod
    def store_key(num_a, num_b):
        sorted_nums = sorted([num_a, num_b])
        return f"{sorted_nums[0]}_{sorted_nums[1]}"

    def steps_between(self, num_start, num_end):
        key = Maze.store_key(num_start, num_end)
        if key not in self.steps_between_store:
            pos_start = self.number_locations()[num_start]
            pos_end = self.number_locations()[num_end]
            distance = self.find_distance(pos_start, pos_end)
            self.steps_between_store[key] = distance
        return self.steps_between_store[key]

    def find_distance(self, pos_a, pos_b):
        start_state = Position(self.maze, pos_a, pos_b)
        end_state = a_star.a_star(start_state, tag_func=lambda x: str(x.current_pos))
        return end_state.previous_steps


def get_char(maze, pos):
    return maze[pos[0]][pos[1]]


class Position(a_star.State):
    def __init__(self, maze, current_pos, end_pos, previous_steps=0) -> None:
        self.maze = maze
        self.end_pos = end_pos
        self.current_pos = current_pos
        self.previous_steps = previous_steps
        super().__init__()

    def is_valid(self):
        if np.any(self.current_pos < 0):
            return False
        if np.any(self.current_pos >= self.maze.shape):
            return False
        current_char = get_char(self.maze, self.current_pos)
        if current_char == WALL_CHAR:
            return False
        return True

    def is_complete(self):
        return np.all(self.current_pos == self.end_pos)

    def all_possible_next_states(self):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if (dx and dy) or (dx == dy == 0):
                    continue
                yield Position(
                    self.maze,
                    self.current_pos + np.array((dx, dy)),
                    self.end_pos,
                    self.previous_steps + 1,
                )

    def __lt__(self, other):
        return self.previous_steps < other.previous_steps

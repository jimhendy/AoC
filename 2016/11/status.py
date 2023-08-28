import itertools

import numpy as np
from items import Microchip


class Status:
    def __init__(self, contents, current_elevator_floor=1, prev_steps=0) -> None:
        self.contents = contents
        self.elevator_floor = current_elevator_floor
        self.prev_steps = prev_steps
        self.n_items = sum([len(v) for v in self.contents.values()])

    def __repr__(self) -> str:
        size = [len(v) for v in self.contents.values()]
        total = np.sum(size)
        return f"{self.prev_steps}, {self.elevator_floor}, {size}, {total}, {self._mean_level():,.2f}"

    def metric(self):
        # How many potentails moves away from finishing
        items_by_floor = {k: len(v) for k, v in self.contents.items()}
        current_floor = self.elevator_floor
        top_floor = len(self.contents)
        steps = 0
        while items_by_floor[top_floor] != self.n_items:
            lowest_occupied = min([f for f, i in items_by_floor.items() if i])
            # Get to this floor
            steps += current_floor - lowest_occupied
            items_by_floor[current_floor] -= 1
            items_by_floor[lowest_occupied] += 1

            # Take two items to the top floor
            steps += top_floor - lowest_occupied
            items_by_floor[top_floor] += 2
            items_by_floor[lowest_occupied] -= 2

            current_floor = top_floor
            pass
        return self.prev_steps + steps

    def _mean_level(self):
        levels = [
            floor for floor, contents in self.contents.items() for item in contents
        ]
        return np.mean(levels)

    def __lt__(self, other):
        return self.metric() < other.metric()

    def __gt__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return self.contents == other.contents

    def is_valid(self):
        for floor_content in self.contents.values():
            chips = []
            gens = []
            for i in floor_content:
                if isinstance(i, Microchip):
                    chips.append(i)
                else:
                    gens.append(i)
            if not len(gens):
                continue
            g_names = [g.name for g in gens]
            for m in chips:
                if m.name not in g_names:
                    return False
        return True

    def is_complete(self):
        return all(
            len(contents) == 0
            for floor, contents in self.contents.items()
            if floor != 4
        )

    def all_possible_next_states(self):
        current_items = self.contents[self.elevator_floor]

        # Can either take 1 or 2 generators, 1 or 2 microchips or matching generator & microchip
        chips = []
        gens = []
        for i in current_items:
            if isinstance(i, Microchip):
                chips.append(i)
            else:
                gens.append(i)

        matching_sets = [{m, g} for m in chips for g in gens if m.name == g.name]
        two_generators = list(map(set, itertools.combinations(gens, 2)))
        two_microchips = list(map(set, itertools.combinations(chips, 2)))
        # Combine all these sets
        possible_content = (
            [{i} for i in current_items]
            + matching_sets
            + two_generators
            + two_microchips
        )
        # Could go to any other floor but each delta 1 is considered a move
        possible_floors = [
            i for i in self.contents if abs(i - self.elevator_floor) == 1
        ]

        for dest_floor in possible_floors:
            for moving_items in possible_content:
                new_contents = self.contents.copy()
                new_contents[dest_floor] = new_contents[dest_floor].union(moving_items)
                new_contents[self.elevator_floor] = new_contents[
                    self.elevator_floor
                ].difference(moving_items)
                yield Status(new_contents, dest_floor, self.prev_steps + 1)

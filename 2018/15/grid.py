import os
from collections import defaultdict

import a_star
import exceptions
import units
from location import Location

CHARS = {"Wall": "#", "Space": ".", "Elf": "E", "Goblin": "G"}
PATH_CACHE = {}

class Grid:
    def __init__(self, input_grid, elf_power=3):
        self.elf_power = elf_power
        self.grid = self.create_gird(input_grid)
        self.unit_counts = defaultdict(int)
        self.units = []
        self.initial_find_units()
        self.rounds = 0

    def initial_find_units(self):
        for r, row in enumerate(self.grid):
            for c, char in enumerate(row):
                if char == CHARS["Elf"]:
                    self.add_unit(units.Elf(Location(r, c), self, attack_power=self.elf_power))
                elif char == CHARS["Goblin"]:
                    self.add_unit(units.Goblin(Location(r, c), self))

    def do_round(self):
        units = sorted(self.units, key=lambda u: u.loc)
        for u in units:
            if u.hit_points <= 0:
                continue
            u.take_turn()
        if any([v == 0 for v in self.unit_counts.values()]):
            raise exceptions.GameOverException
        self.rounds += 1

    def create_gird(self, input_grid):
        return [list(l) for l in input_grid.split(os.linesep)]

    def add_unit(self, unit):
        self.unit_counts[unit.symbol] += 1
        self.units.append(unit)

    def kill_unit(self, unit):
        self.unit_counts[unit.symbol] -= 1
        self.set_char(unit.loc, CHARS["Space"])
        self.units.remove(unit)

    def move_unit(self, unit, new_loc):
        self.set_char(unit.loc, CHARS["Space"])
        unit.loc = new_loc
        self.set_char(unit.loc, unit.symbol)

    def locate_targets(self, attacking_unit):
        return [u.loc for u in self.units if u.symbol == attacking_unit.enemy_symbol]

    def find_paths(self, starting_pos, targets):
        key = self.get_key(starting_pos, targets)
        if key in PATH_CACHE.keys():
            return PATH_CACHE[key]
        loc_to_steps = []
        for t in targets:
            try:
                shortest_path = a_star.a_star(
                    PathState([starting_pos], t, self),
                    tag_func=lambda s: s.prev_steps[-1].tup,
                )
                loc_to_steps.append(shortest_path)
            except a_star.AStarException:
                # No path available
                pass
        PATH_CACHE[key] = loc_to_steps
        return loc_to_steps

    def get_key(self, start, targets):
        key = start.tup.__repr__()
        for t in targets:
            key += '-' + t.__repr__()
        key += '=' + self.get_str_grid()
        return key

    def get_str_grid(self):
        return os.linesep.join(
            [''.join(line) for line in self.grid]
        )

    def print_grid(self):
        print(self.get_str_grid())

    def get_char(self, loc):
        return self.grid[loc.row][loc.col]

    def set_char(self, loc, char):
        self.grid[loc.row][loc.col] = char


class PathState(a_star.State):
    def __init__(self, prev_steps, target_pos, grid):
        self.prev_steps = prev_steps  # Should include starting loc
        self.target_pos = target_pos
        self.grid = grid

    def is_valid(self):
        return True

    def is_complete(self):
        return self.prev_steps[-1] == self.target_pos

    def all_possible_next_states(self):
        for al in adjacent_locs(self.prev_steps[-1]):
            if self.grid.get_char(al) != CHARS["Space"]:
                continue
            new_prev_steps = self.prev_steps + [al]
            yield PathState(
                prev_steps=new_prev_steps, target_pos=self.target_pos, grid=self.grid
            )

    def __lt__(self, other):
        steps_diff = len(self.prev_steps) - len(other.prev_steps)
        if steps_diff == 0:
            return self.prev_steps[-1] < other.prev_steps[-1]
        else:
            return steps_diff < 0

    ## ==================================


def adjacent_locs(loc):
    locs = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr and dc:
                continue
            locs.append(Location(loc.row + dr, loc.col + dc))
    return locs

from collections import defaultdict

import exceptions
import grid
from location import Location

DEBUG = False


class Unit:
    def __init__(self, loc, grid, symbol, enemy_symbol, attack_power=3):
        self.symbol = symbol
        self.enemy_symbol = enemy_symbol
        self.attack_power = attack_power
        self.hit_points = 200
        self.loc = loc  # Location(row, col)
        self.grid = grid

    def take_turn(self):
        target_locs = self.grid.locate_targets(self)
        if not len(target_locs):
            if DEBUG:
                print("No targets found")
            # raise NoTargetsException
            return
        adjacent_locs = self.find_adjacent_locs(target_locs)
        if not len(adjacent_locs):
            if DEBUG:
                print("No valid adjacent locations")
            # raise NoPossibleAdjacentLocsException
            return
        paths = self.grid.find_paths(self.loc, adjacent_locs)
        if not len(paths):
            if DEBUG:
                print("No valid paths")
            # raise NoPossiblePathsException
            return
        path_lengths = defaultdict(list)
        for p in paths:
            path_lengths[len(p.prev_steps)].append(p)
        min_path_length = min(path_lengths.keys())
        if min_path_length != 1:
            min_path = sorted(
                path_lengths[min_path_length], key=lambda p: p.prev_steps[-1]
            )[0]
            self.move(min_path.prev_steps[1])
        self.attack()

    def move(self, new_loc):
        if DEBUG:
            print(f"Moving to {new_loc.__repr__()}")
        self.grid.move_unit(self, new_loc)

    def attack(self):
        targets = []
        for al in grid.adjacent_locs(self.loc):
            if self.grid.get_char(al) == self.enemy_symbol:
                targets.append([u for u in self.grid.units if u.loc == al][0])
        if not len(targets):
            return
        hit_points = defaultdict(list)
        for t in targets:
            hit_points[t.hit_points].append(t)
        min_hit_points = min(hit_points.keys())
        target = sorted(hit_points[min_hit_points], key=lambda t: t.loc)[0]
        target.get_attacked(self)

    def get_attacked(self, attacking_unit):
        self.hit_points -= attacking_unit.attack_power
        if self.hit_points <= 0:
            self.grid.kill_unit(self)

    def find_adjacent_locs(self, target_locs):
        adj_locs = []
        for tl in target_locs:
            for new_loc in grid.adjacent_locs(tl):
                if new_loc == self.loc:
                    # Already in attacking position
                    return [new_loc]
                try:
                    new_char = self.grid.get_char(new_loc)
                    if new_char == grid.CHARS["Space"]:
                        adj_locs.append(new_loc)
                except IndexError:
                    # new_loc is outside grid range
                    pass
        return adj_locs

    def __repr__(self):
        return f"{self.symbol} [{self.loc.__repr__()}]"


class Elf(Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol="E", enemy_symbol="G")


class Goblin(Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, symbol="G", enemy_symbol="E")

import os
import numpy as np
from typing import List, Union, Dict, Tuple
import numba
from numba.experimental import jitclass
import logging

# numba_logger = logging.getLogger("numba")
# numba_logger.setLevel(logging.DEBUG)


# ROOM_ID_TO_DESIRED = list("ABCD")
TYPE_TO_COST = {"A": 1, "B": 10, "C": 100, "D": 1_000}
TYPE_TO_TYPE_ID = {"A": 0, "B": 1, "C": 2, "D": 3}
# FORBIDDEN_HALLWAY_POS = np.array([2, 4, 6, 8])
# HALLWAY_POS_TO_ROOM_ID = {2: 0, 4: 1, 6: 2, 8: 3}
# ROOM_ID_TO_HALLWAY_POS = {v: k for k, v in HALLWAY_POS_TO_ROOM_ID.items()}
# EMPTY_CHAR = -1
# AMPHIPOD_ID_TO_TYPE = {}
# AMPHIPOD_ID_TO_COST = {}

spec = [
    ("hallway", numba.types.int32[:]),
    ("rooms", numba.types.int32[:, :]),
    ("entered_room_amphipod_ids", numba.types.boolean[:]),
    ("energy", numba.types.int32),
    ("amphipod_id_to_type", numba.types.int32[:]),
    ("amphipod_id_to_cost", numba.types.int32[:]),
]


@jitclass(spec)
class Route:
    def __init__(
        self,
        hallway,
        rooms,
        entered_room_amphipod_ids,
        energy,
        amphipod_id_to_type,
        amphipod_id_to_cost,
    ):
        self.hallway = hallway
        self.rooms = rooms
        self.entered_room_amphipod_ids = entered_room_amphipod_ids
        self.energy = energy
        self.amphipod_id_to_type = amphipod_id_to_type
        self.amphipod_id_to_cost = amphipod_id_to_cost

    @staticmethod
    def room_id_to_desired(room_id):
        if room_id == 0:
            return "A"
        elif room_id == 1:
            return "B"
        elif room_id == 2:
            return "C"
        else:
            return "D"

    @staticmethod
    def hallway_pos_to_room_id(hallway_pos):
        if hallway_pos == 2:
            return 0
        elif hallway_pos == 4:
            return 1
        elif hallway_pos == 6:
            return 2
        else:
            return 3

    @staticmethod
    def room_id_to_hallway_pos(room_id):
        if room_id == 0:
            return 2
        elif room_id == 1:
            return 4
        elif room_id == 2:
            return 6
        else:
            return 8

    def is_complete(self):
        if not np.all(self.hallway == -1):
            return False
        for i in range(len(self.rooms)):
            for c in self.rooms[i]:
                if self.amphipod_id_to_type[c] != i:
                    return False
        return True

    def is_valid(self):
        return True

    def __lt__(self, other):
        return self.energy < other.energy

    def tag(self):
        # return np.hstack([self.hallway, self.rooms.reshape(1, -1)[0]])

        s = np.empty(
            self.hallway.shape[0] + self.rooms.shape[0] * self.rooms.shape[1],
            dtype=np.int32,
        )
        for i in range(len(self.hallway)):
            s[i] = self.hallway[i]
        for i in range(len(self.rooms)):
            for j in range(len(self.rooms[i])):
                s[self.hallway.shape[0] + i * self.rooms.shape[1] + j] = self.rooms[
                    i, j
                ]
        # return s
        mult = np.power(10, np.arange(len(s)))
        return np.multiply(s, mult).sum()

    def all_possible_next_states(self):
        occupied = set([i for i, c in enumerate(self.hallway) if c != -1])
        outputs = []

        # Hallway chaps can move to other hallway spots or into empty rooms (can't pass each other)
        for hallway_pos in range(len(self.hallway)):

            amphipod_id = self.hallway[hallway_pos]

            if amphipod_id == -1:
                continue

            for new_pos in range(len(self.hallway)):

                if new_pos in occupied:
                    continue
                elif new_pos < hallway_pos:
                    crossing_other = False
                    for o in occupied:
                        if new_pos < o and o < hallway_pos:
                            crossing_other = True
                            break
                else:
                    crossing_other = False
                    for o in occupied:
                        if new_pos > o and o > hallway_pos:
                            crossing_other = True
                            break
                if crossing_other:
                    continue

                if new_pos in np.array([2, 4, 6, 8], dtype=np.int32):
                    # Go from hallway into a room

                    room_id = self.hallway_pos_to_room_id(new_pos)
                    if self.amphipod_id_to_type[amphipod_id] != room_id:
                        continue

                    room = self.rooms[room_id]

                    if not np.any(room == -1):
                        continue

                    vacancy = -1
                    correct_type = True
                    for i in range(len(room)):
                        if room[i] == -1:
                            vacancy = i
                        elif room[i] != room_id:
                            correct_type = False
                            break
                    
                    if not correct_type:
                        continue

                    new_rooms = self.rooms.copy()
                    new_rooms[room_id, vacancy] = amphipod_id

                    new_hallway = self.hallway.copy()
                    new_hallway[hallway_pos] = -1

                    extra_energy = self.amphipod_id_to_cost[amphipod_id] * vacancy
                    new_entered_ids = self.entered_room_amphipod_ids.copy()
                    new_entered_ids[amphipod_id] = True

                    outputs.append(
                        Route(
                            new_hallway,
                            new_rooms,
                            new_entered_ids,
                            self.energy
                            + np.abs(new_pos - hallway_pos)
                            * self.amphipod_id_to_cost[amphipod_id]
                            + self.amphipod_id_to_cost[amphipod_id]
                            + extra_energy,
                            self.amphipod_id_to_type,
                            self.amphipod_id_to_cost,
                        )
                    )
                else:
                    # Go from one hallway position to another
                    new_hallway = self.hallway.copy()
                    new_hallway[hallway_pos] = -1
                    new_hallway[new_pos] = amphipod_id

                    new_rooms = self.rooms.copy()

                    outputs.append(
                        Route(
                            new_hallway,
                            new_rooms,
                            self.entered_room_amphipod_ids.copy(),
                            self.energy
                            + self.amphipod_id_to_cost[amphipod_id]
                            * np.abs(new_pos - hallway_pos),
                            self.amphipod_id_to_type,
                            self.amphipod_id_to_cost,
                        )
                    )

        # Room chaps can move out only if the have not already done so
        for room_id, room in enumerate(self.rooms):

            next_amphipod_id = [(i, c) for i, c in enumerate(room) if c != -1]
            if not len(next_amphipod_id):
                continue
            room_space = next_amphipod_id[0][0]
            amphipod_id = next_amphipod_id[0][1]

            if self.entered_room_amphipod_ids[amphipod_id]:
                continue

            for new_pos in range(len(self.hallway)):
                room_pos = self.room_id_to_hallway_pos(room_id)

                if new_pos in occupied:
                    continue
                elif new_pos in np.array([2, 4, 6, 8], dtype=np.int32):
                    continue
                elif new_pos < room_pos:
                    crossing_other = False
                    for o in occupied:
                        if new_pos < o and o < room_pos:
                            crossing_other = True
                            break
                else:
                    crossing_other = False
                    for o in occupied:
                        if new_pos > o and o > room_pos:
                            crossing_other = True
                            break
                if crossing_other:
                    continue

                new_rooms = self.rooms.copy()
                new_rooms[room_id, room_space] = -1

                extra_energy = self.amphipod_id_to_cost[amphipod_id] * room_space

                new_hallway = self.hallway.copy()
                new_hallway[new_pos] = amphipod_id

                outputs.append(
                    Route(
                        new_hallway,
                        new_rooms,
                        self.entered_room_amphipod_ids.copy(),
                        self.energy
                        + np.abs(new_pos - room_pos)
                        * self.amphipod_id_to_cost[amphipod_id]
                        + self.amphipod_id_to_cost[amphipod_id]
                        + extra_energy,
                        self.amphipod_id_to_type,
                        self.amphipod_id_to_cost,
                    )
                )
        return outputs


import heapq

DEBUG = False


class AStarException(Exception):
    pass


def a_star(
    initial_state, tag_func=str, return_status=False, test_tag_at_best_option=False
):
    """Perform the A* search algorithm
    The initial_state should be a subclass of State (below)
    that implements:
    - is_complete - boolean of whether this state is the desired result
    - is_valid - boolean
    - all_possible_next_states - iterable of states after this one

    Arguments:
        initial_state {user_class with above methods}

    Keyword Arguments:
        tag_func {callable} -- [function to tag each
        state with so we can know if it has already been seen
        ] (default: {str})

        return_status {boolean} -- Rather than returning the
        final state, return a dictionary summarising the search

    Returns:
        [user_class(State)] -- [Desired search result]
    """

    i = 0
    possible_states = [(initial_state[0], i)]
    data = {i: initial_state[1]}
    seen = set()
    n_tests = 0
    is_complete = False

    while len(possible_states):

        _, best_option_key = heapq.heappop(possible_states)
        best_option = data.pop(best_option_key)
        n_tests += 1

        if test_tag_at_best_option:
            tag = tag_func(best_option)
            if tag in seen:
                if DEBUG:
                    print(f"Skipping {tag} as already seen")
                continue
            seen.add(tag)

        if best_option.energy == 440:
            if best_option.hallway[3] == 2 and best_option.hallway.sum() == -8:
                print(best_option.hallway)
                print(best_option.rooms)
                print(best_option.energy)

                print()

        if not best_option.energy % 100:
            print(best_option.energy)
        if DEBUG:
            print(
                f"Test {n_tests}, n_options {len(possible_states)}, best_option: {tag_func(best_option)}"
            )
        if best_option.is_complete():
            if DEBUG:
                print("Search complete")
            is_complete = True
            break

        for s in best_option.all_possible_next_states():
            tag = s.tag()
            if tag in seen:
                continue
            i += 1
            data[i] = s
            key = (s.energy, i)
            heapq.heappush(possible_states, key)

    if return_status:
        return {
            "seen": seen,
            "best_option": best_option,
            "n_tests": n_tests,
            "is_complete": is_complete,
        }
    elif is_complete:
        return best_option
    else:
        raise AStarException("Search did not complete")


def run(inputs):
    lines = inputs.split(os.linesep)
    hallway = np.full(lines[1].count("."), -1, dtype=np.int32)

    top_amphipods = lines[2].replace("#", "").strip()
    top_middle = "DCBA"
    bottom_middle = "DBAC"
    bottom_amphipods = lines[3].replace("#", "").strip()

    all_amphipods = [
        j
        for i in [top_amphipods, top_middle, bottom_middle, bottom_amphipods]
        for j in i
    ]

    amphipod_id_to_type = np.empty(len(all_amphipods), dtype=np.int32)
    amphipod_id_to_cost = np.empty_like(amphipod_id_to_type, dtype=np.int32)

    for amphipod_id, amphipod_type in enumerate(all_amphipods):
        amphipod_id_to_type[amphipod_id] = TYPE_TO_TYPE_ID[amphipod_type]
        amphipod_id_to_cost[amphipod_id] = TYPE_TO_COST[amphipod_type]

    rooms = (
        np.arange(len(all_amphipods), dtype=np.int32).reshape(-1, len(top_amphipods)).T
    )

    entered_room_amphioid_id = np.full_like(amphipod_id_to_cost, False, dtype=bool)

    initial_state = Route(
        hallway=hallway,
        rooms=rooms,
        entered_room_amphipod_ids=entered_room_amphioid_id,
        energy=0,
        amphipod_id_to_type=amphipod_id_to_type,
        amphipod_id_to_cost=amphipod_id_to_cost,
    )

    best_route = a_star(
        initial_state=(0, initial_state),
        test_tag_at_best_option=True,
        tag_func=lambda x: str(x.tag()),
    )
    print(best_route)
    return best_route.energy

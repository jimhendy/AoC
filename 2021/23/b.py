import heapq
import os

import numba
import numpy as np
from numba.experimental import jitclass

TYPE_TO_COST = {"A": 1, "B": 10, "C": 100, "D": 1_000}
TYPE_TO_TYPE_ID = {"A": 0, "B": 1, "C": 2, "D": 3}

spec = [
    ("hallway", numba.types.int32[:]),
    ("rooms", numba.types.int32[:, :]),
    ("energy", numba.types.int32),
    ("amphipod_id_to_type", numba.types.int32[:]),
    ("amphipod_id_to_cost", numba.types.int32[:]),
    ("rooms_complete", numba.types.boolean[:]),
    ("vacancies", numba.types.int32[:]),
    ("next_space_to_leave", numba.types.int32[:]),
]


@jitclass(spec)
class Route:
    def __init__(
        self,
        hallway,
        rooms,
        energy,
        amphipod_id_to_type,
        amphipod_id_to_cost,
    ) -> None:
        self.hallway = hallway
        self.rooms = rooms
        self.energy = energy
        self.amphipod_id_to_type = amphipod_id_to_type
        self.amphipod_id_to_cost = amphipod_id_to_cost
        self.rooms_complete = self._analyse_rooms_complete()
        self.vacancies = self._analyse_vacancies()
        self.next_space_to_leave = self._analyse_leaving()

    def _analyse_rooms_complete(self):
        complete = np.full(self.rooms.shape[0], True)
        for i, r in enumerate(self.rooms):
            for a in r:
                if a == -1 or self.amphipod_id_to_type[a] != i:
                    complete[i] = False
                    break
        return complete

    def _analyse_vacancies(self):
        vacancies = np.full(self.rooms.shape[0], -1, dtype=np.int32)
        for i, r in enumerate(self.rooms):
            if self.rooms_complete[i]:
                continue
            wrong_type_present = False
            for a in r:
                if a != -1 and self.amphipod_id_to_type[a] != i:
                    wrong_type_present = True
                    break
            if wrong_type_present:
                continue
            for j, a in enumerate(r):
                if a == -1:
                    vacancies[i] = j
        return vacancies

    def _analyse_leaving(self):
        leaving = np.full(self.rooms.shape[0], -1, dtype=np.int32)
        for i, r in enumerate(self.rooms):
            if self.rooms_complete[i]:
                continue
            max_incorrect_space = -1
            for j, a in enumerate(r):
                if a != -1 and self.amphipod_id_to_type[a] != i:
                    max_incorrect_space = j
            for j, a in enumerate(r):
                if j > max_incorrect_space:
                    break
                if a != -1:
                    leaving[i] = j
                    break
        return leaving

    @staticmethod
    def hallway_pos_to_room_id(hallway_pos):
        if hallway_pos == 2:
            return 0
        elif hallway_pos == 4:
            return 1
        elif hallway_pos == 6:
            return 2
        elif hallway_pos == 8:
            return 3
        else:
            return 100

    @staticmethod
    def room_id_to_hallway_pos(room_id):
        if room_id == 0:
            return 2
        elif room_id == 1:
            return 4
        elif room_id == 2:
            return 6
        elif room_id == 3:
            return 8
        else:
            return 100

    def is_complete(self):
        return np.all(self.rooms_complete)

    def tag(self):
        s = np.empty(
            self.hallway.shape[0] + self.rooms.shape[0] * self.rooms.shape[1],
            dtype=np.int32,
        )
        for i, a in enumerate(self.hallway):
            if a == -1:
                s[i] = a
            else:
                s[i] = self.amphipod_id_to_type[a]
        loc = i + 1
        for r in self.rooms:
            for a in r:
                if a == -1:
                    s[loc] = a
                else:
                    s[loc] = self.amphipod_id_to_type[a]
                loc += 1
        return s

    def print(self):
        s = "#" * (len(self.hallway) + 2) + os.linesep + "#"
        for h in self.hallway:
            if h == -1:
                s += " "
            else:
                s += str(self.amphipod_id_to_type[h])
        s += "#"
        for i in range(self.rooms.shape[1]):
            s += os.linesep + " "
            for j in range(len(self.hallway)):
                if j in [2, 4, 6, 8]:
                    r = self.rooms[self.hallway_pos_to_room_id(j)]
                    type = r[i]
                    if type == -1:
                        s += " "
                    else:
                        s += str(self.amphipod_id_to_type[type])
                else:
                    s += " "
            s += " "
        print(s)

    def all_possible_next_states(self):
        occupied = [i for i, c in enumerate(self.hallway) if c != -1]
        outputs = []

        # Hallway chaps can move into their room if it's ready
        for hallway_pos, amphipod_id in enumerate(self.hallway):
            if amphipod_id == -1:
                continue

            amphipod_type = self.amphipod_id_to_type[amphipod_id]
            room_id = amphipod_type

            if self.vacancies[room_id] == -1:
                continue

            room_pos = self.room_id_to_hallway_pos(room_id)

            crossing_other = False
            if room_pos < hallway_pos:
                for o in occupied:
                    if room_pos < o and o < hallway_pos:
                        crossing_other = True
                        break
            else:
                for o in occupied:
                    if room_pos > o and o > hallway_pos:
                        crossing_other = True
                        break
            if crossing_other:
                continue

            room = self.rooms[room_id]

            new_rooms = self.rooms.copy()
            new_rooms[room_id, self.vacancies[room_id]] = amphipod_id

            new_hallway = self.hallway.copy()
            new_hallway[hallway_pos] = -1

            cost = self.amphipod_id_to_cost[amphipod_id]
            in_energy = cost * (self.vacancies[room_id] + 1)
            move_energy = np.abs(room_pos - hallway_pos) * cost

            outputs.append(
                Route(
                    new_hallway,
                    new_rooms,
                    self.energy + move_energy + in_energy,
                    self.amphipod_id_to_type,
                    self.amphipod_id_to_cost,
                ),
            )

        # Room chaps can move out only if the have not already done so
        for room_id, room in enumerate(self.rooms):
            if self.next_space_to_leave[room_id] == -1:
                continue

            room_space = self.next_space_to_leave[room_id]
            if room_space == -1:
                continue
            amphipod_id = room[room_space]
            room_pos = self.room_id_to_hallway_pos(room_id)

            for new_pos in range(len(self.hallway)):
                if new_pos in occupied:
                    continue
                elif new_pos == room_pos:
                    continue

                crossing_other = False
                if new_pos < room_pos:
                    for o in occupied:
                        if new_pos < o and o < room_pos:
                            crossing_other = True
                            break
                else:
                    for o in occupied:
                        if new_pos > o and o > room_pos:
                            crossing_other = True
                            break
                if crossing_other:
                    continue

                if new_pos in np.array([2, 4, 6, 8], dtype=np.int32):
                    # Go from room into destination room

                    dest_room_id = self.hallway_pos_to_room_id(new_pos)
                    if self.amphipod_id_to_type[amphipod_id] != dest_room_id:
                        continue

                    vacancy = self.vacancies[dest_room_id]
                    if vacancy == -1:
                        continue

                    new_rooms = self.rooms.copy()
                    new_rooms[dest_room_id, vacancy] = amphipod_id
                    new_rooms[room_id, room_space] = -1

                    cost = self.amphipod_id_to_cost[amphipod_id]
                    out_energy = cost * (room_space + 1)
                    in_energy = cost * (vacancy + 1)
                    move_energy = cost * np.abs(new_pos - room_pos)

                    outputs.append(
                        Route(
                            self.hallway,
                            new_rooms,
                            self.energy + move_energy + in_energy + out_energy,
                            self.amphipod_id_to_type,
                            self.amphipod_id_to_cost,
                        ),
                    )
                else:
                    # Go from room into hallway
                    new_rooms = self.rooms.copy()
                    new_rooms[room_id, room_space] = -1

                    cost = self.amphipod_id_to_cost[amphipod_id]
                    extra_energy = cost * (room_space + 1)
                    move_energy = cost * np.abs(new_pos - room_pos)

                    new_hallway = self.hallway.copy()
                    new_hallway[new_pos] = amphipod_id

                    outputs.append(
                        Route(
                            new_hallway,
                            new_rooms,
                            self.energy + move_energy + extra_energy,
                            self.amphipod_id_to_type,
                            self.amphipod_id_to_cost,
                        ),
                    )
        return outputs


def a_star(initial_state, tag_func=str):
    """Custom implementation required as numba jitclass instances can't be used in the heapq."""
    i = 0
    possible_states = [(initial_state[0], i)]
    data = {i: initial_state[1]}
    tags = {i: tag_func(initial_state[1])}
    seen = set()

    while len(possible_states):
        _, best_option_key = heapq.heappop(possible_states)
        best_option = data.pop(best_option_key)

        if tags[best_option_key] in seen:
            continue
        seen.add(tags[best_option_key])

        if best_option.is_complete():
            return best_option

        for s in best_option.all_possible_next_states():
            tag = tag_func(s)
            if tag in seen:
                continue
            i += 1
            data[i] = s
            tags[i] = tag
            key = (s.energy, i)
            heapq.heappush(possible_states, key)

    msg = "Search did not complete"
    raise RuntimeError(msg)


def run(inputs):
    lines = inputs.split(os.linesep)
    hallway = np.full(lines[1].count("."), -1, dtype=np.int32)

    top_amphipods = lines[2].replace("#", "").strip()
    top_middle = "DCBA"
    bottom_middle = "DBAC"
    bottom_amphipods = lines[3].replace("#", "").strip()

    all_inputs = [top_amphipods, top_middle, bottom_middle, bottom_amphipods]
    all_amphipods = [j for i in all_inputs for j in i]

    amphipod_id_to_type = np.empty(len(all_amphipods), dtype=np.int32)
    amphipod_id_to_cost = np.empty_like(amphipod_id_to_type, dtype=np.int32)

    for amphipod_id, amphipod_type in enumerate(all_amphipods):
        amphipod_id_to_type[amphipod_id] = TYPE_TO_TYPE_ID[amphipod_type]
        amphipod_id_to_cost[amphipod_id] = TYPE_TO_COST[amphipod_type]

    rooms = (
        np.arange(len(all_amphipods), dtype=np.int32).reshape(-1, len(top_amphipods)).T
    )

    initial_state = Route(
        hallway=hallway,
        rooms=rooms,
        energy=0,
        amphipod_id_to_type=amphipod_id_to_type,
        amphipod_id_to_cost=amphipod_id_to_cost,
    )

    def tag_state(route):
        return tuple(route.tag())

    best_route = a_star(
        initial_state=(0, initial_state),
        tag_func=tag_state,
    )

    return best_route.energy

import os

import numpy as np

from tools.a_star import State, a_star


class Amphipod:
    def __init__(
        self,
        type: str,
        id_number: int,
        hallway_pos: None | int = None,
        entered_room: bool = False,
    ) -> None:
        self.type = type
        self.cost = {"A": 1, "B": 10, "C": 100, "D": 1_000}[type]
        self.hallway_pos = hallway_pos
        self.entered_room = entered_room
        self.id_number = id_number

    def copy(self) -> "Amphipod":
        return Amphipod(
            type=self.type,
            hallway_pos=self.hallway_pos,
            entered_room=self.entered_room,
            id_number=self.id_number,
        )

    def __repr__(self) -> str:
        return f"{self.type}, {self.cost}, {self.hallway_pos}, {self.entered_room}, {self.id_number}"


class Hallway:
    def __init__(self, length: int, occupied: dict[int, int] | None = None) -> None:
        self.length = length
        self.occupied = (
            {}
            if occupied is None
            else occupied  # hallway position(int, zero based) to Amphipod id_number
        )

    def move_amphipod(self, old: int, new: int, amphipod_id: int) -> "Hallway":
        assert new not in self.occupied
        new_occupied = {k: v for k, v in self.occupied.items() if k != old}
        new_occupied[new] = amphipod_id
        return Hallway(length=self.length, occupied=new_occupied)

    def copy(self) -> "Hallway":
        return Hallway(
            length=self.length,
            occupied=dict(self.occupied.items()),
        )


class Room:
    def __init__(
        self,
        top_amphipod_id: None | int,
        bottom_amphipod_id: None | int,
        hallway_pos: int,
        desired_type: str,
    ) -> None:
        self.top_amphipod_id = top_amphipod_id
        self.bottom_amphipod_id = bottom_amphipod_id
        self.hallway_pos = hallway_pos
        self.desired_type = desired_type

    def can_add(self, amphipod: Amphipod, all_amphipods: list[Amphipod]) -> bool:
        if amphipod.type != self.desired_type:
            return False
        if self.bottom_amphipod_id is None:
            return True
        if self.top_amphipod_id is not None:
            return False
        bottom = next(
            a for a in all_amphipods if a.id_number == self.bottom_amphipod_id
        )
        return amphipod.type == bottom.type

    def add_amphipod(self, amphipod_id: int) -> "Room":
        if self.bottom_amphipod_id is None:
            return Room(
                top_amphipod_id=None,
                bottom_amphipod_id=amphipod_id,
                hallway_pos=self.hallway_pos,
                desired_type=self.desired_type,
            )
        elif self.top_amphipod_id is None:
            return Room(
                top_amphipod_id=amphipod_id,
                bottom_amphipod_id=self.bottom_amphipod_id,
                hallway_pos=self.hallway_pos,
                desired_type=self.desired_type,
            )
        else:
            msg = "No space to add a new amphipod"
            raise RuntimeError(msg)

    def __repr__(self) -> str:
        return f"{self.top_amphipod_id}_{self.bottom_amphipod_id}"

    def get_next_amphipod_id(self) -> int | None:
        if self.top_amphipod_id is not None:
            return self.top_amphipod_id
        elif self.bottom_amphipod_id is not None:
            return self.bottom_amphipod_id
        else:
            return None

    def copy(self) -> "Room":
        return Room(
            top_amphipod_id=self.top_amphipod_id,
            bottom_amphipod_id=self.bottom_amphipod_id,
            hallway_pos=self.hallway_pos,
            desired_type=self.desired_type,
        )

    def is_complete(self, all_amphipods: list[Amphipod]) -> bool:
        if self.top_amphipod_id is None or self.bottom_amphipod_id is None:
            return False
        top_type = next(
            a for a in all_amphipods if a.id_number == self.top_amphipod_id
        ).type
        bottom_type = next(
            a for a in all_amphipods if a.id_number == self.bottom_amphipod_id
        ).type
        return top_type == bottom_type == self.desired_type


class Route(State):
    def __init__(
        self,
        hallway: Hallway,
        rooms: list[Room],
        amphipods: list[Amphipod],
        energy: int = 0,
        history: None | list[tuple[int, str]] = None,
    ) -> None:
        self.hallway = hallway

        self.rooms = rooms
        self.amphipods = amphipods
        self.energy = energy
        self.history = history if history is not None else []
        self.history.append((self.energy, self.__repr__()))

    def is_complete(self):
        return all(r.is_complete(all_amphipods=self.amphipods) for r in self.rooms)

    def is_valid(self):
        return True

    def __lt__(self, other):
        return self.energy < other.energy

    def _amphipod_from_id(self, id_number: int) -> str:
        return next(a for a in self.amphipods if a.id_number == id_number)

    def __repr__(self) -> str:
        s = "#" * (self.hallway.length + 2) + os.linesep + "#"
        for hallway_pos in range(self.hallway.length):
            if hallway_pos in self.hallway.occupied:
                s += self._amphipod_from_id(self.hallway.occupied[hallway_pos]).type
            else:
                s += "."
        s += "#" + os.linesep + "#"
        for pos in range(self.hallway.length):
            found = False
            for r in self.rooms:
                if r.hallway_pos == pos:
                    top = r.top_amphipod_id
                    if top is None:
                        s += " "
                    else:
                        s += self._amphipod_from_id(top).type
                    found = True
                    break
            if not found:
                s += " "
        s += "#" + os.linesep + "#"
        for pos in range(self.hallway.length):
            found = False
            for r in self.rooms:
                if r.hallway_pos == pos:
                    bottom = r.bottom_amphipod_id
                    if bottom is None:
                        s += " "
                    else:
                        s += self._amphipod_from_id(bottom).type
                    found = True
                    break
            if not found:
                s += " "
        s += "#"
        return s

    def all_possible_next_states(self):
        # Hallway chaps can move to other hallway spots or into empty rooms (can't pass each other)
        occupied = sorted(self.hallway.occupied.keys())
        for hallway_pos, amphipod_id in self.hallway.occupied.items():
            amphipod = next(a for a in self.amphipods if a.id_number == amphipod_id)
            if amphipod.entered_room:
                msg = "Shouldn't have dudes in the hallway that have already entered a room"
                raise RuntimeError(
                    msg,
                )

            for new_pos in range(self.hallway.length):
                # if any([new_pos == r.hallway_pos for r in self.rooms]):
                if new_pos == hallway_pos or new_pos in occupied:
                    continue
                elif new_pos < hallway_pos:
                    crossing_other = any(new_pos < i < hallway_pos for i in occupied)
                else:
                    crossing_other = any(new_pos > i > hallway_pos for i in occupied)
                if crossing_other:
                    continue

                outside_room = [r for r in self.rooms if r.hallway_pos == new_pos]
                if len(outside_room):
                    assert len(outside_room) == 1
                    r = outside_room[0]
                    if not r.can_add(amphipod=amphipod, all_amphipods=self.amphipods):
                        continue
                    new_room = r.add_amphipod(amphipod_id=amphipod.id_number)
                    new_amphipod = amphipod.copy()
                    new_amphipod.hallway_pos = None
                    new_amphipod.entered_room = True

                    new_rooms = [rr.copy() for rr in self.rooms if r is not rr]
                    new_rooms.append(new_room)

                    new_amphipods = [a.copy() for a in self.amphipods if a != amphipod]
                    new_amphipods.append(new_amphipod)

                    new_hallway = self.hallway.copy()
                    del new_hallway.occupied[hallway_pos]

                    is_bottom = new_room.top_amphipod_id is None
                    extra_energy = amphipod.cost if is_bottom else 0

                    yield Route(
                        hallway=new_hallway,
                        rooms=new_rooms,
                        amphipods=new_amphipods,
                        energy=self.energy
                        + np.abs(new_pos - hallway_pos) * amphipod.cost
                        + amphipod.cost
                        + extra_energy,
                        history=self.history[:],
                    )
                else:
                    new_hallway = self.hallway.move_amphipod(
                        old=hallway_pos,
                        new=new_pos,
                        amphipod_id=amphipod.id_number,
                    )
                    new_rooms = [r.copy() for r in self.rooms]
                    new_amphipods = [a.copy() for a in self.amphipods if a != amphipod]
                    new_moved_amphiod = amphipod.copy()
                    new_moved_amphiod.hallway_pos = new_pos
                    new_amphipods.append(new_moved_amphiod)

                    yield Route(
                        hallway=new_hallway,
                        rooms=new_rooms,
                        amphipods=new_amphipods,
                        energy=self.energy
                        + amphipod.cost * np.abs(new_pos - hallway_pos),
                        history=self.history[:],
                    )

        # Room chaps can move out only if the have not already done so
        for r in self.rooms:
            next_amphipod_id = r.get_next_amphipod_id()
            if next_amphipod_id is None:
                continue
            next_amphipod = next(
                a for a in self.amphipods if a.id_number == next_amphipod_id
            )
            if next_amphipod.entered_room:
                continue
            for new_pos in range(self.hallway.length):
                if new_pos in occupied:
                    continue
                elif any(rr.hallway_pos == new_pos for rr in self.rooms):
                    continue
                elif new_pos < r.hallway_pos:
                    crossing_other = any(new_pos < i < r.hallway_pos for i in occupied)
                else:
                    crossing_other = any(new_pos > i > r.hallway_pos for i in occupied)
                if crossing_other:
                    continue

                new_rooms = [rr.copy() for rr in self.rooms if rr is not r]
                new_room = r.copy()
                if new_room.top_amphipod_id is not None:
                    new_room.top_amphipod_id = None
                    extra_energy = 0
                else:
                    new_room.bottom_amphipod_id = None
                    extra_energy = next_amphipod.cost
                new_rooms.append(new_room)

                new_hallway = self.hallway.copy()
                new_hallway.occupied[new_pos] = next_amphipod_id

                new_amphipods = [a.copy() for a in self.amphipods if a != next_amphipod]
                new_amphipod = next_amphipod.copy()
                new_amphipod.hallway_pos = new_pos
                new_amphipods.append(new_amphipod)

                yield Route(
                    hallway=new_hallway,
                    rooms=new_rooms,
                    amphipods=new_amphipods,
                    energy=self.energy
                    + np.abs(new_pos - r.hallway_pos) * next_amphipod.cost
                    + next_amphipod.cost
                    + extra_energy,
                    history=self.history[:],
                )


def run(inputs):
    lines = inputs.split(os.linesep)
    hallway = Hallway(length=lines[1].count("."))

    top_amphipods = lines[2].replace("#", "").strip()
    bottom_amphipods = lines[3].replace("#", "").strip()

    amphipods = [
        Amphipod(type=t, id_number=i)
        for i, t in enumerate(list(top_amphipods) + list(bottom_amphipods))
    ]
    print(list(amphipods))

    rooms = [
        Room(
            top_amphipod_id=i,
            bottom_amphipod_id=i + len(top_amphipods),
            hallway_pos=h,
            desired_type=t,
        )
        for i, (h, t) in enumerate([(2, "A"), (4, "B"), (6, "C"), (8, "D")])
    ]

    initial_state = Route(hallway=hallway, rooms=rooms, amphipods=amphipods)

    best_route = a_star(initial_state=initial_state, tag_func=lambda x: x.__repr__())

    print(best_route.energy)
    for h in best_route.history:
        print(h[1])
    print()

    return best_route.energy

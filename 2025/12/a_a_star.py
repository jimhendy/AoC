from collections.abc import Iterable
from dataclasses import dataclass

from tools.a_star import AStarError, a_star
from tools.a_star import State as _State


@dataclass
class Shape:
    id: int
    points: set[complex]

    def all_orientations(self):
        """
        Rotate and flip the shape to get all unique orientations.
        Yield each unique orientation as a set of complex numbers.
        """
        seen = set()
        current = self.points

        for _ in range(4):
            # Rotate 90 degrees
            current = {p * 1j for p in current}
            if frozenset(current) not in seen:
                seen.add(frozenset(current))
                yield self._move_to_origin(current)
            # # Flip horizontally
            # flipped = {complex(-p.real, p.imag) for p in current}
            # if frozenset(flipped) not in seen:
            #     seen.add(frozenset(flipped))
            #     yield flipped
            # # Flip vertically
            # flipped_v = {complex(p.real, -p.imag) for p in current}
            # if frozenset(flipped_v) not in seen:
            #     seen.add(frozenset(flipped_v))
            #     yield flipped_v

    @staticmethod
    def _move_to_origin(points: set[complex]) -> set[complex]:
        min_x = min(p.real for p in points)
        min_y = min(p.imag for p in points)
        return {p - complex(min_x, min_y) for p in points}

    @classmethod
    def from_input(cls, input: str) -> "Shape":
        """
        0:
        ###
        ##.
        ##.

        Output id: 0, points: {0+0j, 1+0j, 2+0j, 0+1j, 1+1j, 0+2j, 1+2j}
        """
        lines = input.splitlines()
        shape_id = int(lines[0].rstrip(":"))
        points = set()
        for y, line in enumerate(lines[1:]):
            for x, char in enumerate(line):
                if char == "#":
                    points.add(complex(x, y))
        return cls(shape_id, points)


@dataclass
class Region:
    width: int
    height: int
    required_shapes: dict[int, int]  # shape_id -> count

    @classmethod
    def from_input(cls, input: str) -> "Region":
        """
        12x5: 1 0 1 0 3 2

        Output width: 12, height: 5, required_shapes: {0:1, 1: 0, 2:1, 3:0, 4:3, 5:2}
        """
        size_part, shapes_part = input.split(":")
        width, height = map(int, size_part.split("x"))
        shape_counts = list(map(int, shapes_part.strip().split()))
        required_shapes = {i: count for i, count in enumerate(shape_counts)}
        return cls(width, height, required_shapes)


class State(_State):
    def __init__(
        self,
        region: Region,
        shapes: list[Shape],
        placed_shapes: dict[int, int],
        grid: set[complex],
    ):
        self.region = region
        self.shapes = shapes
        self.placed_shapes = placed_shapes  # shape_id -> count placed
        self.grid = grid  # occupied points in the region
        # Log
        # print(f"Initialized State: placed_shapes={self.placed_shapes}, occupied={len(self.grid)} points")
        # self.print()

    def is_complete(self) -> bool:
        return all(
            self.placed_shapes.get(sid, 0) == count
            for sid, count in self.region.required_shapes.items()
        )

    def all_possible_next_states(self) -> Iterable["State"]:
        for shape in self.shapes:
            placed_count = self.placed_shapes.get(shape.id, 0)
            required_count = self.region.required_shapes.get(shape.id, 0)
            if placed_count >= required_count:
                continue  # Already placed enough of this shape
            # print(f"Trying to place shape {shape.id}, placed {placed_count}/{required_count}")
            # print(f"Current grid occupied: {len(self.grid)} points")
            # self.print()
            for orientation in shape.all_orientations():
                max_x = max(p.real for p in orientation)
                max_y = max(p.imag for p in orientation)
                # print(f"Trying orientation with max_x={max_x}, max_y={max_y}, points={orientation}")
                # breakpoint()
                for x_offset in range(self.region.width - int(max_x)):
                    for y_offset in range(self.region.height - int(max_y)):
                        translated_shape = {
                            p + complex(x_offset, y_offset) for p in orientation
                        }
                        if not translated_shape & self.grid:  # No overlap
                            new_grid = self.grid | translated_shape
                            new_placed_shapes = self.placed_shapes.copy()
                            new_placed_shapes[shape.id] = placed_count + 1
                            yield State(
                                self.region, self.shapes, new_placed_shapes, new_grid,
                            )

    def is_valid(self) -> bool:
        return True  # All generated states are valid by construction

    def __lt__(self, other: "State") -> bool:
        return sum(self.placed_shapes.values()) < sum(other.placed_shapes.values())

    def __repr__(self) -> str:
        return f"{self.placed_shapes}, occupied: {len(self.grid)}"

    def print(self) -> None:
        grid_repr = [
            ["." for _ in range(self.region.width)] for _ in range(self.region.height)
        ]
        for point in self.grid:
            x, y = int(point.real), int(point.imag)
            grid_repr[y][x] = "#"
        for line in grid_repr:
            print("".join(line))
        print()


def run(input: str) -> int:
    shapes: list[Shape] = []
    regions: list[Region] = []

    input_sections = input.strip().split("\n\n")
    for section in input_sections:
        if "#" in section:
            shape = Shape.from_input(section)
            shapes.append(shape)
        else:
            for region in section.split("\n"):
                regions.append(Region.from_input(region))

    total = 0

    for region in regions:
        initial_state = State(region, shapes, {}, set())
        try:
            solution = a_star(initial_state)
            print("Solution found:")
            solution.print()
            total += 1
        except AStarError:
            print("No solution found.")
        # break

    return total

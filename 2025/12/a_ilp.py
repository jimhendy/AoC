from dataclasses import dataclass

import cvxpy as cp


@dataclass
class Shape:
    id: int
    points: set[complex]

    def all_orientations(self):
        """Generate all unique orientations (8 possible: 4 rotations × 2 reflections)."""
        seen = set()

        def add_if_unique(points):
            normalized = self._move_to_origin(points)
            frozen = frozenset(normalized)
            if frozen not in seen:
                seen.add(frozen)
                yield normalized

        current = self.points

        # 4 rotations
        for _ in range(4):
            yield from add_if_unique(current)
            current = {p * 1j for p in current}

        # Flip horizontally and do 4 more rotations
        flipped = {complex(-p.real, p.imag) for p in self.points}
        for _ in range(4):
            yield from add_if_unique(flipped)
            flipped = {p * 1j for p in flipped}

    @staticmethod
    def _move_to_origin(points: set[complex]) -> set[complex]:
        if not points:
            return points
        min_x = min(p.real for p in points)
        min_y = min(p.imag for p in points)
        return {p - complex(min_x, min_y) for p in points}

    @classmethod
    def from_input(cls, input: str) -> "Shape":
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
    required_shapes: dict[int, int]

    @classmethod
    def from_input(cls, input: str) -> "Region":
        size_part, shapes_part = input.split(":")
        width, height = map(int, size_part.split("x"))
        shape_counts = list(map(int, shapes_part.strip().split()))
        required_shapes = {i: count for i, count in enumerate(shape_counts)}
        return cls(width, height, required_shapes)


def solve_ilp(region: Region, shapes: list[Shape]) -> bool:
    """
    Solve tiling problem using Integer Linear Programming.

    Key insight: Cells can be covered AT MOST once (not exactly once),
    allowing for empty cells in the grid.

    Variables: x[i] = 1 if placement i is used

    Constraints:
    1. Each cell covered at most once (allows empty cells)
    2. Each shape used exactly required_shapes[s] times
    """
    # Generate all valid placements (shape_id, orientation, position, occupied_cells)
    print(f"Generating placements for region {region.width}x{region.height}")
    placements = []

    for shape in shapes:
        for orientation in shape.all_orientations():
            max_x = max(p.real for p in orientation)
            max_y = max(p.imag for p in orientation)

            # Try all positions where shape fits within bounds
            for x_off in range(region.width - int(max_x)):
                for y_off in range(region.height - int(max_y)):
                    occupied = []
                    valid = True

                    for p in orientation:
                        x = int(p.real) + x_off
                        y = int(p.imag) + y_off
                        if x >= region.width or y >= region.height:
                            valid = False
                            break
                        occupied.append((x, y))

                    if valid:
                        placements.append({"shape_id": shape.id, "cells": occupied})

    if not placements:
        return False

    # Decision variables: binary for each placement
    n_placements = len(placements)
    x = cp.Variable(n_placements, integer=True, nonneg=True, bounds=[0, 1])

    constraints = []

    # Constraint 1: Each cell covered at most once (key change from "== 1" to "<= 1")
    for i in range(region.width):
        for j in range(region.height):
            covering = [idx for idx, p in enumerate(placements) if (i, j) in p["cells"]]
            if covering:
                constraints.append(cp.sum(x[covering]) <= 1)

    # Constraint 2: Each shape used exactly required times
    for shape_id, required_count in region.required_shapes.items():
        if required_count > 0:
            shape_placements = [
                idx for idx, p in enumerate(placements) if p["shape_id"] == shape_id
            ]
            if shape_placements:
                constraints.append(cp.sum(x[shape_placements]) == required_count)

    # Solve for feasibility
    objective = cp.Minimize(cp.sum(x))
    problem = cp.Problem(objective, constraints)

    try:
        # Try specialized integer solvers first, fall back to default
        for solver_name in [cp.GLPK_MI, cp.CBC, cp.SCIP]:
            try:
                problem.solve(solver=solver_name, verbose=False)
                if problem.status == cp.OPTIMAL:
                    return True
            except cp.SolverError:
                continue

        # Try default solver
        problem.solve(verbose=False)
        return problem.status == cp.OPTIMAL

    except Exception:
        return False


def run(input: str) -> int:
    """Count how many regions can be successfully tiled with the given shapes."""
    shapes: list[Shape] = []
    regions: list[Region] = []

    # Parse input: shapes have "#" in them, regions are dimension specifications
    input_sections = input.strip().split("\n\n")
    for section in input_sections:
        if "#" in section:
            shapes.append(Shape.from_input(section))
        else:
            for region_line in section.split("\n"):
                regions.append(Region.from_input(region_line))

    # Count solvable regions
    return sum(1 for region in regions if solve_ilp(region, shapes))

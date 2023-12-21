from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, eq=True)
class Beam:
    location: complex
    direction: complex


def empty_space(beam: Beam) -> list[Beam]:
    return [
        Beam(beam.location + beam.direction, beam.direction),
    ]


def forward_mirror(beam: Beam) -> list[Beam]:
    if beam.direction.real == 1:
        new_direction = complex(0, -1)
    elif beam.direction.real == -1:
        new_direction = complex(0, 1)
    elif beam.direction.imag == 1:
        new_direction = complex(-1, 0)
    elif beam.direction.imag == -1:
        new_direction = complex(1, 0)
    else:
        raise ValueError(f"Unexpected direction: {beam.direction}")
    return [
        Beam(beam.location + new_direction, new_direction),
    ]


def backward_mirror(beam: Beam) -> list[Beam]:
    if beam.direction.real == 1:
        new_direction = complex(0, 1)
    elif beam.direction.real == -1:
        new_direction = complex(0, -1)
    elif beam.direction.imag == 1:
        new_direction = complex(1, 0)
    elif beam.direction.imag == -1:
        new_direction = complex(-1, 0)
    else:
        raise ValueError(f"Unexpected direction: {beam.direction}")
    return [
        Beam(beam.location + new_direction, new_direction),
    ]


def vertical_split(beam: Beam) -> list[Beam]:
    if beam.direction.imag:
        return [
            Beam(beam.location + beam.direction, beam.direction),
        ]
    return [
        Beam(beam.location + complex(0, direction), complex(0, direction))
        for direction in (1, -1)
    ]


def horizontal_split(beam: Beam) -> list[Beam]:
    if beam.direction.real:
        return [
            Beam(beam.location + beam.direction, beam.direction),
        ]
    return [
        Beam(beam.location + complex(direction, 0), complex(direction, 0))
        for direction in (1, -1)
    ]


def run(inputs: str) -> int:
    max_x, max_y = 0, 0

    grid: dict[complex, str] = {}
    for y, line in enumerate(inputs.splitlines()):
        max_y = max(max_y, y)
        for x, character in enumerate(line):
            max_x = max(max_x, x)
            grid[complex(x, y)] = character

    beams = set([Beam(complex(0, 0), complex(1, 0))])
    beam_heads = deque(beams)

    while beam_heads:
        beam = beam_heads.popleft()

        grid_character = grid.get(beam.location, ".")

        propagate = {
            "/": forward_mirror,
            "\\": backward_mirror,
            "|": vertical_split,
            "-": horizontal_split,
            ".": empty_space,
        }[grid_character]

        for new_beam in propagate(beam):
            if not (0 <= new_beam.location.real <= max_x):
                continue
            if not (0 <= new_beam.location.imag <= max_y):
                continue
            if new_beam in beams:
                continue
            beams.add(new_beam)
            beam_heads.append(new_beam)

    return len(set(beam.location for beam in beams))

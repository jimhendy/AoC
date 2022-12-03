import os
import re

import a_star
from items import Generator, Microchip
from status import Status


def _int_from_str(s):
    return {"first": 1, "second": 2, "third": 3, "fourth": 4}.get(s)


def run(inputs):
    contents_by_floor = {}
    for line in inputs.split(os.linesep):
        floor = re.findall(r"^The (\w+) floor", line)[0]
        floor_int = _int_from_str(floor)
        contents_by_floor[floor_int] = set(
            [Generator(n) for n in re.findall(r"(\w+) generator", line)]
            + [Microchip(n) for n in re.findall(r"(\w+)\-compatible microchip", line)]
        )

    initial_state = Status(contents_by_floor)
    result = a_star.a_star(initial_state, lambda x: f"{x.elevator_floor}{x.contents}")

    return result.prev_steps

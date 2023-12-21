from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Lens:
    label: str
    focal_length: int

    def __eq__(self, label: str) -> bool:
        return self.label == label


def _hash(step: str) -> int:
    current_value = 0
    for character in step:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


def remove_lens(
    boxes: dict[int, deque[Lens]],
    label: str,
):
    box = boxes[_hash(label)]
    try:
        box.remove(label)
    except ValueError:
        pass


def insert_lens(
    boxes: dict[int, deque[Lens]],
    label: str,
    focal_length: int,
):
    box = boxes[_hash(label)]
    new_lens = Lens(label, focal_length)
    try:
        current_index = box.index(label)
        box[current_index] = new_lens
    except ValueError:
        box.append(new_lens)


def total_focussing_power(boxes: dict[int, deque[Lens]]) -> int:
    total = 0
    for box_num, lenses in boxes.items():
        for lens_num, lens in enumerate(lenses, start=1):
            total += (box_num + 1) * lens_num * lens.focal_length
    return total


def run(inputs: str) -> int:
    boxes = defaultdict(deque[Lens])
    for step in inputs.splitlines()[0].split(","):
        if "=" in step:
            label, focal_length = step.split("=")
            insert_lens(
                boxes,
                label,
                int(focal_length),
            )
        else:
            label = step[:-1]
            remove_lens(
                boxes,
                label,
            )
    return total_focussing_power(boxes)

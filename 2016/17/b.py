import hashlib
import re

import a_star
import numpy as np

STEPS = {
    "U": np.array([0, +1]),
    "D": np.array([0, -1]),
    "L": np.array([-1, 0]),
    "R": np.array([+1, 0]),
}


class Position(a_star.State):
    def __init__(self, pos, passcode) -> None:
        self.pos = pos
        self.passcode = passcode

    def __lt__(self, other):
        return len(self.passcode) > len(other.passcode)

    def is_valid(self):
        return True

    def is_complete(self):
        return False

    def _hash(self):
        return hashlib.md5(self.passcode.encode()).hexdigest()

    def all_possible_next_states(self):
        if not np.all(self.pos == [3, -3]):
            new_hash = self._hash()[:4]
            for s, h in zip(STEPS.items(), new_hash):
                new_pos = self.pos + s[1]
                if (
                    (new_pos[0] < 0)
                    | (new_pos[1] > 0)
                    | (new_pos[0] > 3)
                    | (new_pos[1] < -3)
                ):
                    continue
                if h not in ["b", "c", "d", "e", "f"]:
                    continue
                yield Position(pos=new_pos, passcode=self.passcode + s[0])


def run(inputs):
    initial_state = Position(np.array([0, 0]), inputs)
    result = a_star.a_star(
        initial_state,
        tag_func=lambda x: f"{x.passcode}_{x.pos}",
        return_status=True,
    )

    successful_codes = []
    for s in result["seen"]:
        if s.endswith("_[ 3 -3]"):
            successful_codes.append(s.split("_")[0])

    best = sorted(successful_codes, key=len)[-1]
    return len(re.sub(f"^{inputs}", "", best))

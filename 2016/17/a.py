import hashlib
import a_star
import numpy as np
import re

STEPS = {
    "U": np.array([0, +1]),
    "D": np.array([0, -1]),
    "L": np.array([-1, 0]),
    "R": np.array([+1, 0]),
}


class Position(a_star.State):
    def __init__(self, pos, passcode):
        self.pos = pos
        self.passcode = passcode

    def __lt__(self, other):
        return len(self.passcode) < len(other.passcode)

    def is_valid(self):
        return True

    def is_complete(self):
        return np.all(self.pos == [3, -3])

    def _hash(self):
        return hashlib.md5(self.passcode.encode()).hexdigest()

    def all_possible_next_states(self):
        new_hash = self._hash()[:4]
        for s, h in zip(STEPS.items(), new_hash):
            new_pos = self.pos + s[1]
            if (
                (new_pos[0] < 0)
                | (new_pos[1] > 0)
                | (new_pos[0] > 3)
                | (new_pos[1] < -3)
            ):
                # print(f'Pos not valid "{new_pos}"')
                continue
            if h not in ["b", "c", "d", "e", "f"]:
                # print(f'Hash not valid "{h}" for "{new_pos}"')
                continue
            # print(f'** Yielding {new_pos}')
            yield Position(pos=new_pos, passcode=self.passcode + s[0])
        # print('-'*40)


def run(inputs):

    initial_state = Position(np.array([0, 0]), inputs)
    result = a_star.a_star(initial_state, tag_func=lambda x: x.passcode)

    return re.sub(f"^{inputs}", "", result.passcode)

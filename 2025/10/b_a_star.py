import heapq
import re
from collections.abc import Iterable
from dataclasses import dataclass

from tools.a_star import AStarError
from tools.a_star import State as _State

"""
Sample input:
[##...#] (1,3,4,5) (2,3,5) (0,2,3) (0,2,3,4,5) (1,2,4) (0,1,2,3) {24,27,40,30,25,17}
[#....] (0,2) (0,1,4) (0) (0,4) (0,3,4) (0,1,2,3) {53,16,16,24,27}
[#####.###] (4,6) (0,5,6,8) (0,1,3,5,6,8) (0,1,2,3,4,5,7,8) (2,3) (1,2,3,4,6,7) (0,2,5,6,8) (2,3,4,5) (0,1,2,3,5,6,8) {168,164,176,171,51,173,194,30,168}
[..##] (1,3) (0,2,3) (0,1) (2,3) {30,15,29,34}
[....#.#.] (0,1,5) (2,4,6) (2,3) (2,3,7) (0,1,4,5,6,7) (0,2,3,4,5,6) {25,14,42,28,32,25,32,13}
[.###] (0,1,2,3) (1,2,3) {0,9,9,9}
"""

REGEX = re.compile(
    r"\[(?P<lights>[.#]+)\](?P<buttons>(?: \([0-9,]+\))+?) \{(?P<aim>[0-9, ]+)\}",
)


@dataclass(frozen=True, slots=True, kw_only=True)
class State(_State):
    aim: tuple[int]
    buttons: tuple[tuple[int, ...], ...]
    joltage: tuple[int]
    aim_index: int
    n_pushes: int = 0
    _heuristic: int = None

    def is_complete(self) -> bool:
        return self.joltage == self.aim

    def all_possible_next_states(self) -> Iterable["State"]:
        for b in self.buttons:
            overshoot = False
            for j in b:
                if self.joltage[j] >= self.aim[j]:
                    overshoot = True
                    break
            if overshoot:
                continue

            new_joltage_list = list(self.joltage)
            for j in b:
                new_joltage_list[j] += 1

            new_joltage = tuple(new_joltage_list)
            h = max(self.aim[i] - new_joltage[i] for i in range(len(self.aim)))

            yield State(
                aim=self.aim,
                buttons=self.buttons,
                joltage=new_joltage,
                n_pushes=self.n_pushes + 1,
                aim_index=self.aim_index,
                _heuristic=h,
            )

    def is_valid(self) -> bool:
        return True

    def h1(self) -> int:
        if self._heuristic is None:
            return max(self.aim[i] - self.joltage[i] for i in range(len(self.aim)))
        return self._heuristic

    def __lt__(self, other: _State) -> bool:
        return (self.n_pushes + self._heuristic) < (other.n_pushes + other._heuristic)

    def __repr__(self) -> str:
        return str(self.joltage)

    def is_valid_intermediate(self) -> bool:
        """
        Return True if this state is a valid intermediate state to yield in an iterative a_star.
        """
        if self.aim[self.aim_index] == self.joltage[self.aim_index]:
            # print(f"  Reached aim at index {self.aim_index} with joltage {self.joltage[self.aim_index]}")
            return True
        return False


def a_star_iterative(initial_state: State):
    """
    Like a_star search but yield any state where State.is_valid_intermediate() is True.
    """
    possible_states = [initial_state]
    seen = set()

    while possible_states:
        best_option = heapq.heappop(possible_states)

        tag = best_option.joltage
        if tag in seen:
            continue
        seen.add(tag)

        if best_option.is_complete():
            yield best_option
            return

        if best_option.is_valid_intermediate():
            yield best_option
            continue

        for s in best_option.all_possible_next_states():
            heapq.heappush(possible_states, s)

    msg = "Search did not complete"
    raise AStarError(msg)


def recursive_a_star(
    all_buttons: list[set[int]],
    aim_index_to_n_buttons: list[tuple[int, int]],
    aim_index_pos: int,
    current_state: State,
) -> State:
    # Base case: we've satisfied all aim indices
    if aim_index_pos >= len(aim_index_to_n_buttons):
        if current_state.is_complete():
            return current_state
        raise AStarError(
            f"Reached end of aim indices but state not complete: {current_state.joltage} vs {current_state.aim}",
        )

    aim_index, _ = aim_index_to_n_buttons[aim_index_pos]
    # print(f"Solving for aim index {aim_index} (current joltage: {current_state.joltage}, aim: {current_state.aim})")

    relevant_buttons = [b for b in all_buttons if aim_index in b]

    for intermediate_state in a_star_iterative(
        State(
            aim=current_state.aim,
            buttons=relevant_buttons,
            joltage=current_state.joltage,
            n_pushes=current_state.n_pushes,
            aim_index=aim_index,
        ),
    ):
        try:
            # print(f"  Found intermediate state {intermediate_state} for aim index {aim_index}")
            next_state = State(
                aim=intermediate_state.aim,
                buttons=all_buttons,
                joltage=intermediate_state.joltage,
                n_pushes=intermediate_state.n_pushes,
                aim_index=intermediate_state.aim_index,
            )
            result_state = recursive_a_star(
                all_buttons,
                aim_index_to_n_buttons,
                aim_index_pos + 1,
                next_state,
            )
            return result_state
        except AStarError:
            # print(f"  No solution found from intermediate state {intermediate_state}, trying next.")
            pass
    raise AStarError(f"No solution found for aim index {aim_index}")


# @profile
def run(input: str) -> int:
    total = 0
    for line in input.splitlines():
        print(f"Processing line: {line}")
        match = REGEX.match(line)

        if not match:
            msg = f"Line does not match expected format: {line}"
            raise ValueError(msg)

        buttons_str = match.group("buttons").strip().split(" ")
        aim_str = match.group("aim")

        buttons = tuple(
            tuple(sorted(map(int, b[1:-1].split(",")))) for b in buttons_str
        )
        aim = tuple(map(int, aim_str.split(",")))

        # Iterate through the values in the aim, yielding an a_star result for each
        # Start with the joltage that has the fewest buttons which can contribute to it
        # This will reduce the space and improve solve time

        aim_index_to_n_buttons = {
            i: len([b for b in buttons if i in b]) for i in range(len(aim))
        }
        aim_index_buttons = sorted(aim_index_to_n_buttons.items(), key=lambda x: x[1])

        # For each aim_index, run an a_star_iterative to reach that aim. Yield that best option
        # and try to reach the next aim_index from there.
        initial_h = max(aim)
        initial_state = State(
            aim=aim,
            buttons=buttons,
            joltage=tuple([0] * len(aim)),
            n_pushes=0,
            aim_index=0,
            _heuristic=initial_h,
        )
        solution = recursive_a_star(
            all_buttons=buttons,
            aim_index_to_n_buttons=aim_index_buttons,
            aim_index_pos=0,
            current_state=initial_state,
        )

        total += solution.n_pushes

    return total

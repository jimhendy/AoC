import multiprocessing as mp
from dataclasses import dataclass
from functools import cache

import regex as re

DAMAGED_REGEX = re.compile("#+")
DAMAGED_OR_UNKNOWN = r"[#\?]"
EMPTY_OR_UNKNOWN = r"[\?\.]"
CACHE: dict[str, list[str]] = {}


@cache
def is_valid_state(state: str, damaged_springs: tuple[int]) -> bool:
    regex = f"^{EMPTY_OR_UNKNOWN}*?"
    for num_damaged in damaged_springs[:-1]:
        regex += f"{DAMAGED_OR_UNKNOWN}{{{num_damaged}}}{EMPTY_OR_UNKNOWN}+?"
    if damaged_springs:
        regex += f"{DAMAGED_OR_UNKNOWN}{{{damaged_springs[-1]}}}"
    regex += f"{EMPTY_OR_UNKNOWN}*?$"

    try:
        # Potential catastrphic backtracking so we timeout
        return bool(re.match(regex, state, timeout=1e-1))
    except TimeoutError:
        return False


@dataclass(slots=True)
class SpringRow:
    initial_state: str
    damaged_springs: list[int]

    @staticmethod
    def split_completed_runs(state: str, completed_runs: list[int]) -> list[str]:
        if not completed_runs:
            return ["", state]
        regex = r"(^\.*"
        for num_damaged in completed_runs:
            regex += rf"#{{{num_damaged}}}\.+"
        regex += ")"
        group = re.compile(regex).findall(state)[0]
        before, after = state[: len(group)], state[len(group) :]
        # print(f"Splitting {state} into {before} and {after} for {completed_runs}")
        return [before, after]

    def _cache_key(self) -> str:
        return self.initial_state + ",".join(map(str, self.damaged_springs))

    # @profile
    def solutions(self) -> list[str]:
        # print(f"Calculating solutions for {self.initial_state}, {self.damaged_springs}")
        cache_key = self._cache_key()

        if cache_key not in CACHE:
            solutions = 0

            if "?" not in self.initial_state:
                # No more damaged springs
                solutions = 1

            else:
                # We have more damaged springs
                # Replace the first unknown (?) with a "." and a "#" and try again

                # Find the index of the first "?"
                unknown_location = self.initial_state.index("?")
                before_unknown = self.initial_state[:unknown_location]

                # Find how many completed runs are contained in the starting string
                potential_completed_runs = [
                    len(i) for i in before_unknown.split(".") if i
                ]
                completed_runs = []
                for potential, expected in zip(
                    potential_completed_runs,
                    self.damaged_springs,
                    strict=False,
                ):
                    if potential == expected:
                        completed_runs.append(potential)
                    else:
                        break
                if completed_runs and before_unknown.endswith("#"):
                    completed_runs = completed_runs[:-1]
                # print(f"Removing {completed_runs=}")

                # Split the self.initial_state into the completed runs and unknown component
                before, after = SpringRow.split_completed_runs(
                    self.initial_state,
                    completed_runs,
                )

                if completed_runs:
                    if not self.damaged_springs:
                        raise Exception(
                            f"No more damaged springs but {len(completed_runs)=}",
                        )
                    damaged_springs = self.damaged_springs[len(completed_runs) :]
                else:
                    damaged_springs = self.damaged_springs
                damaged_springs = tuple(damaged_springs)

                for replacement_char in ".#":
                    new_state = after.replace("?", replacement_char, 1)
                    if is_valid_state(new_state, damaged_springs):
                        new_row = SpringRow(new_state, damaged_springs)
                        solutions += new_row.solutions()

            CACHE[cache_key] = solutions

        return CACHE[cache_key]


def return_solutions(spring_row):
    return spring_row.solutions()


def run(inputs: str) -> int:
    lines = inputs.splitlines()

    repeats = 5
    pool = mp.Pool(mp.cpu_count())
    spring_rows = []

    for line in lines:
        state, damaged = line.split()

        state = "?".join([state for _ in range(repeats)])

        damaged_springs = list(map(int, damaged.split(",")))
        damaged_springs = repeats * damaged_springs

        spring_rows.append(SpringRow(state, damaged_springs))

    return sum(pool.map(return_solutions, spring_rows))

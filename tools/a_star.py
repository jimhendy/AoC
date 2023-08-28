import heapq
from abc import ABC, abstractmethod
from collections.abc import Iterable

DEBUG = 0


class AStarException(Exception):
    pass


def a_star(initial_state, tag_func=str, return_status=False):
    """
    Perform the A* search algorithm
    The initial_state should be a subclass of State (below)
    that implements:
    - is_complete - boolean of whether this state is the desired result
    - is_valid - boolean
    - all_possible_next_states - iterable of states after this one.

    Arguments:
    ---------
        initial_state {user_class with above methods}

    Keyword Arguments:
    -----------------
        tag_func {callable} -- [function to tag each
        state with so we can know if it has already been seen
        ] (default: {str})

        return_status {boolean} -- Rather than returning the
        final state, return a dictionary summarising the search

    Returns:
    -------
        [user_class(State)] -- [Desired search result]
    """
    possible_states = [initial_state]
    seen = set()
    n_tests = 0
    is_complete = False

    while len(possible_states):
        best_option = heapq.heappop(possible_states)
        n_tests += 1
        if DEBUG > 0:
            print(
                f"Test {n_tests}, n_options {len(possible_states)}, best_option: {tag_func(best_option)}",
            )
        if best_option.is_complete():
            if DEBUG > 0:
                print("Search complete")
            is_complete = True
            break

        for s in best_option.all_possible_next_states():
            if not s.is_valid():
                if DEBUG > 1:
                    print(f"Skipping {s} as not valid")
                continue
            tag = tag_func(s)
            if tag in seen:
                if DEBUG:
                    print(f"Skipping {tag} as already seen")
                continue
            if DEBUG:
                print("Adding new state to heap")
            seen.add(tag)
            heapq.heappush(possible_states, s)

    if return_status:
        return {
            "seen": seen,
            "best_option": best_option,
            "n_tests": n_tests,
            "is_complete": is_complete,
        }
    elif is_complete:
        return best_option
    else:
        msg = "Search did not complete"
        raise AStarException(msg)


class State(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def is_valid(self) -> bool:
        return False

    @abstractmethod
    def is_complete(self) -> bool:
        return False

    @abstractmethod
    def all_possible_next_states(self) -> Iterable["State"]:
        for _i in range(0):
            yield State()

    @abstractmethod
    def __lt__(self, other: "State") -> bool:
        return True

    def __gt__(self, other: "State") -> bool:
        return not self.__lt__(other)

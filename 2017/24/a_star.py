import heapq
from abc import ABC, abstractmethod
from collections import defaultdict

DEBUG = False


class AStarException(Exception):
    pass


def augmented_a_star(initial_state, return_status=False):
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
        return_status {boolean} -- Rather than returning the
        final state, return a dictionary summarising the search

    Returns:
    -------
        [user_class(State)] -- [Desired search result]
    """
    possible_states = [initial_state]
    n_tests = 0
    is_complete = False
    bridge_data = defaultdict(int)

    while len(possible_states):
        best_option = heapq.heappop(possible_states)
        n_tests += 1
        if best_option.strength > bridge_data[best_option.length]:
            bridge_data[best_option.length] = best_option.strength
        if DEBUG:
            print(f"Test {n_tests:,}, best_option: {best_option}")
            print(f"Current heap size: {len(possible_states):,}")
            print(f"MAX STRENGTH: {max_strength:,}")
        if best_option.is_complete():
            if DEBUG:
                print("Search Complete!")
            is_complete = True
            break

        for s in best_option.all_possible_next_states():
            if not s.is_valid():
                if DEBUG:
                    print(f"Skipping {s} as not valid")
                continue
            if DEBUG:
                print("Adding new state to heap")
            heapq.heappush(possible_states, s)

    if return_status:
        return {
            "best_option": best_option,
            "n_tests": n_tests,
            "is_complete": is_complete,
            "bridge_data": bridge_data,
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
    def is_valid(self):
        return False

    @abstractmethod
    def is_complete(self):
        return False

    @abstractmethod
    def all_possible_next_states(self):
        for _i in range(0):
            yield State()

    @abstractmethod
    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return not self.__lt__(other)

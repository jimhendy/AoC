import heapq
from abc import ABC, abstractmethod

DEBUG = False

"""
In this augmented a_star we allow for a faster route to location
to be found after we have already seen this location.
This is due to the problem not being a simple maze but some steps
taking longer than others.
"""


class AStarException(Exception):
    pass


def augemented_a_star(initial_state, tag_func=str, return_status=False):
    """Perform the A* search algorithm
    The initial_state should be a subclass of State (below)
    that implements:
    - is_complete - boolean of whether this state is the desired result
    - is_valid - boolean
    - all_possible_next_states - iterable of states after this one

    Arguments:
        initial_state {user_class with above methods}

    Keyword Arguments:
        tag_func {callable} -- [function to tag each
        state with so we can know if it has already been seen
        ] (default: {str})

        return_status {boolean} -- Rather than returning the
        final state, return a dictionary summarising the search

    Returns:
        [user_class(State)] -- [Desired search result]
    """

    possible_states = [initial_state]
    seen = {}
    n_tests = 0
    is_complete = False

    while len(possible_states):

        best_option = heapq.heappop(possible_states)
        n_tests += 1
        if DEBUG:
            print(
                f"Test {n_tests}, n_options {len(possible_states)}, best_option: {tag_func(best_option)}"
            )
        if best_option.is_complete():
            if DEBUG:
                print("Search complete")
            is_complete = True
            break

        for s in best_option.all_possible_next_states():
            if not s.is_valid():
                if DEBUG:
                    print(f"Skipping {tag_func(s)} as not valid")
                continue
            tag = tag_func(s)
            if tag in seen:
                if seen[tag] <= s.time:
                    if DEBUG:
                        print(f"Skipping {tag} as already seen with a better time")
                    continue
                else:
                    if DEBUG:
                        print(
                            f"NOT skipping {tag} as we just found a faster way to get there ({s.time} vrs {seen[tag]})"
                        )
            if DEBUG:
                print(f"Adding new state to heap: {tag}")
            seen[tag] = s.time
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
        raise AStarException("Search did not complete")


class State(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def is_valid(self):
        return False

    @abstractmethod
    def is_complete(self):
        return False

    @abstractmethod
    def all_possible_next_states(self):
        for i in range(0):
            yield State()

    @abstractmethod
    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return not self.__lt__(other)

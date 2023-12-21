import heapq
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable

from loguru import logger


class AStarError(Exception):
    pass


def a_star(
    initial_state: "State",
    tag_func: Callable = str,
    *,
    return_status: bool = False,
    debug_mode: bool = False,
):
    """
    Perform the A* search algorithm
    The initial_state should be a subclass of State (below)
    that implements:
    - is_complete - boolean of whether this state is the desired result
    - is_valid - boolean
    - all_possible_next_states - iterable of states after this one.

    Arguments:
    ---------
        initial_state: {user_class with above methods}
        tag_func: {callable} -- [function to tag each
            state with so we can know if it has already been seen
            ]

    Keyword Arguments:
    -----------------
        return_status: {boolean} -- Rather than returning the
            final state, return a dictionary summarising the search
        debug_mode: {boolean} -- Whether to print debug messages

    Returns:
    -------
        [user_class(State)] -- [Desired search result]
    """
    if not debug_mode:
        logger.remove()

    possible_states = [initial_state]
    seen = set()
    n_tests = 0
    is_complete = False

    while possible_states:
        best_option = heapq.heappop(possible_states)
        n_tests += 1
        debug = (
            f"Test {n_tests}, n_options {len(possible_states)}"
            f", best_option: {tag_func(best_option)}",
        )
        logger.debug(debug)
        if best_option.is_complete():
            logger.debug("Search complete")
            is_complete = True
            break

        for s in best_option.all_possible_next_states():
            if not s.is_valid():
                debug = f"Skipping {s} as not valid"
                logger.debug(debug)
                continue
            tag = tag_func(s)
            if tag in seen:
                logger.debug(f"Skipping {tag} as already seen")
                continue
            logger.debug("Adding new state to heap")
            seen.add(tag)
            heapq.heappush(possible_states, s)

    if return_status:
        return {
            "seen": seen,
            "best_option": best_option,
            "n_tests": n_tests,
            "is_complete": is_complete,
        }
    if is_complete:
        return best_option

    msg = "Search did not complete"
    raise AStarError(msg)


class State(ABC):

    """
    A state in the A star search.

    Implement:
    - is_valid
    - is_complete
    - all_possible_next_states
    - __lt__
    """

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

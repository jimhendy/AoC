import heapq


def a_star(initial_state, tag_func=str):
    """Perform the A* search algorithm
    The initial_state should be a class that implements:
    - is_complete - boolean of whether this state is the desired result
    - is_valid - boolean
    - all_possible_next_states - iterable of states after this one

    Arguments:
        initial_state {user_class with above methods}

    Keyword Arguments:
        tag_func {callable} -- [function to tag each
        state with so we can know if it has already been seen
        ] (default: {str})

    Returns:
        [user_class] -- [Desired search result]
    """

    possible_states = [initial_state]
    seen = set()

    while True:

        best_option = heapq.heappop(possible_states)
        if best_option.is_complete():
            break

        for s in best_option.all_possible_next_states():
            if not s.is_valid():
                continue
            tag = tag_func(s)
            if tag in seen:
                continue
            seen.add(tag)
            heapq.heappush(possible_states, s)

    return best_option

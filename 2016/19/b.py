import collections


def run(inputs):
    n_elves = int(inputs)
    near_side = collections.deque()
    far_side = collections.deque()
    for i in range(1, n_elves + 1):
        if i < (n_elves // 2) + 1:
            near_side.append(i)
        else:
            far_side.appendleft(i)

    while near_side and far_side:
        if len(near_side) > len(far_side):
            near_side.pop()
        else:
            far_side.pop()

        # rotate
        far_side.appendleft(near_side.popleft())
        near_side.append(far_side.pop())

    if near_side:
        return near_side[0]
    return far_side[0]

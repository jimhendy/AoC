from collections import deque

def play_round(cups):
    # Current index should be = -1
    current = cups[-1]
    next_three = [cups.popleft() for _ in range(3)]
    
    destination = current -1 or max(cups)
    while destination in next_three:
        destination = destination - 1 or max(cups)

    # Can be faster for large queues
    while cups[-1] != destination:
        cups.rotate(1)

    [ cups.appendleft(i) for i in next_three[::-1] ]
    new_current_index = ( cups.index(current) + 1 ) % len(cups)
    cups.rotate(-new_current_index-1)

def run(inputs):
    cups = deque(map(int, list(inputs)))
    cups.rotate(-1)
    [ play_round(cups) for _ in range(100) ]

    cups.rotate(-cups.index(1))
    cups.popleft()

    return ''.join(map(str, cups))
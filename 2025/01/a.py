from collections import deque

def run(input: str) -> int:
    q = deque(range(100))
    q.rotate(50)
    total = 0
    for line in input.splitlines():
        dir, *n = line
        n = int("".join(n))
        if dir == "L":
            n = -n
        q.rotate(n)
        if not q[0]:
            total += 1
    return total
            
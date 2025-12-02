from collections import deque

def run(input: str) -> int:
    q = deque(range(100))
    q.rotate(50)
    total = 0
    for line in input.splitlines():
        dir, *n = line
        n = int("".join(n))
        step = 1
        if dir == "L":
            step = -1

        for _ in range(n):
            q.rotate(step)
            if not q[0]:
                total += 1
    return total
            
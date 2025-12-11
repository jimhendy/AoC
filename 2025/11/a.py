from collections import deque


def run(input: str) -> int:
    graph = {}
    for line in input.splitlines():
        source, *targets = line.split()
        graph[source[:-1]] = list(targets)

    source = "svr"
    target = "out"
    n_paths = {source: 1}
    stack = deque([source])
    while stack:
        node = stack.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in n_paths:
                stack.append(neighbor)
            n_paths[neighbor] = n_paths.get(neighbor, 0) + n_paths[node]

    return n_paths.get(target, 0)

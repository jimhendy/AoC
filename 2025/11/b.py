from collections import defaultdict, deque


def n_paths(source: str, target: str, graph: dict) -> int:
    """Count directed paths in a DAG via topological DP."""
    nodes = set(graph.keys())
    for destinations in graph.values():
        nodes.update(destinations)

    incoming = {node: 0 for node in nodes}
    for from_, destinations in graph.items():
        for d in destinations:
            incoming[d] += 1

    paths = defaultdict(int)
    paths[source] = 1

    upstreams_analysed = deque(node for node in nodes if not incoming[node])
    while upstreams_analysed:
        from_ = upstreams_analysed.popleft()
        for d in graph.get(from_, []):
            paths[d] += paths[from_]
            incoming[d] -= 1
            if not incoming[d]:
                upstreams_analysed.append(d)

    result = paths.get(target, 0)
    print(f"Number of paths from {source} to {target}: {result}")
    return result


def run(input: str) -> int:
    graph = {}
    for line in input.splitlines():
        source, *targets = line.split()
        graph[source[:-1]] = list(targets)

    svr = "svr"
    out = "out"
    fft = "fft"
    dac = "dac"

    total_paths = 0

    svr_to_fft = n_paths(svr, fft, graph)
    fft_to_dac = n_paths(fft, dac, graph)
    dac_to_out = n_paths(dac, out, graph)
    total_paths += svr_to_fft * fft_to_dac * dac_to_out

    svr_to_dac = n_paths(svr, dac, graph)
    dac_to_fft = n_paths(dac, fft, graph)
    fft_to_out = n_paths(fft, out, graph)
    total_paths += svr_to_dac * dac_to_fft * fft_to_out

    return total_paths

import networkx as nx


def run(inputs: str) -> int:
    graph = nx.DiGraph()
    ordering, updates = inputs.split("\n\n")

    for line in ordering.splitlines():
        nums = line.split("|")
        graph.add_edge(nums[0], nums[1])

    total = 0
    for line in updates.splitlines():
        nums = line.split(",")
        subgraph = graph.subgraph(nums)
        ordered_nodes = {
            node: i for i, node in enumerate(nx.topological_sort(subgraph))
        }
        sorted_nums = sorted(nums, key=ordered_nodes.get)
        if sorted_nums != nums:
            total += int(sorted_nums[len(nums) // 2])

    return total
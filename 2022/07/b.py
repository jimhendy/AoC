import re
from functools import lru_cache
from pathlib import Path

import networkx as nx

REG_CD = re.compile(r"^\$ cd (.+)$")
REG_LS = re.compile(r"^\$ ls$")
REG_OUTPUT_DIR = re.compile("^dir (.+)$")
REG_OUTPUT_FILE = re.compile(r"^(\d+) (.+)$")

TOTAL_SPACE = 70_000_000
UPDATE_SPACE = 30_000_000


@lru_cache(maxsize=1024)
def directory_size(
    directory_name: Path,
    graph: nx.Graph,
    is_root_node: bool = False,
) -> int:
    if is_root_node:
        total = 0
    else:
        parent = directory_name.parent
        total = graph.edges[parent, directory_name]["weight"]
    return total + sum(
        directory_size(s, graph=graph) for s in graph.successors(directory_name)
    )


def run(inputs):
    graph = nx.DiGraph()

    current_directory = None
    directories = []

    for line in inputs.splitlines():
        if reg := REG_CD.findall(line):
            destination = reg[0]
            if destination == "..":
                current_directory = current_directory.parent
            elif current_directory is None:
                current_directory = Path(destination)
            else:
                current_directory /= destination

        elif reg := REG_LS.findall(line):
            continue

        elif reg := REG_OUTPUT_DIR.findall(line):
            sub_dir = current_directory / reg[0]
            graph.add_edge(current_directory, sub_dir, weight=0)
            directories.append(sub_dir)

        elif reg := REG_OUTPUT_FILE.findall(line):
            graph.add_edge(
                current_directory,
                current_directory / reg[0][1],
                weight=int(reg[0][0]),
            )

        else:
            msg = f"Unexpected {line=}"
            raise RuntimeError(msg)

    current_used_space = directory_size(Path("/"), graph, True)
    current_free_space = TOTAL_SPACE - current_used_space
    required_space = UPDATE_SPACE - current_free_space

    possibles = []
    for d in directories:
        size = directory_size(d, graph, True)
        if size >= required_space:
            possibles.append((d, size))

    return sorted(possibles, key=lambda i: i[1])[0][1]

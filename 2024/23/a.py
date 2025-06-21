def run(inputs: str) -> int:
    connections = {line.strip() for line in inputs.splitlines()}

    cycles: set[str] = set()
    for con in connections:
        a, b = con.split("-")
        values = [a, b]
        for other in connections:
            if other == con:
                continue
            c, d = other.split("-")
            this_values = values[:]
            if a == c:
                if f"{b}-{d}" in connections or f"{d}-{b}" in connections:
                    this_values.append(d)
            elif a == d:
                if f"{b}-{c}" in connections or f"{c}-{b}" in connections:
                    this_values.append(c)
            elif b == c:
                if f"{a}-{d}" in connections or f"{d}-{a}" in connections:
                    this_values.append(d)
            elif b == d:
                if f"{a}-{c}" in connections or f"{c}-{a}" in connections:
                    this_values.append(c)

            if len(this_values) == 3 and any(
                node.startswith("t") for node in this_values
            ):
                this_values.sort()
                cycles.add("-".join(this_values))

    return len(cycles)

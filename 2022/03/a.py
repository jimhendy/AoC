def priority(character: str) -> int:
    return ord(character) - (96 if character.islower() else 38)


def run(inputs):
    total = 0

    for line in inputs.splitlines():
        line_len = len(line)
        common = set(line[: line_len // 2]).intersection(set(line[line_len // 2 :]))
        assert len(common) == 1
        total += priority(common.pop())

    return total

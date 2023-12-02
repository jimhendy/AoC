import re

NUMS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def _create_regex(value_regex: str, *, greedy: bool) -> re.Pattern:
    reg = "^.*"
    if not greedy:
        reg += "?"
    reg += f"({value_regex})"
    return re.compile(reg)


def _num_from_line(line: str, regex: re.Pattern, num_values: dict) -> int:
    match = regex.match(line)
    num = match.group(1)
    if num in num_values:
        return num_values[num]
    return int(num)


def run(inputs: str) -> int:
    num_values = {name: value for value, name in enumerate(NUMS, start=1)}

    value_regex = "|".join([*NUMS, r"\d"])

    first_regex = _create_regex(value_regex, greedy=False)
    last_regex = _create_regex(value_regex, greedy=True)

    total = 0
    for line in inputs.splitlines():
        first_num = _num_from_line(line, first_regex, num_values)
        last_num = _num_from_line(line, last_regex, num_values)
        total += int(f"{first_num}{last_num}")

    return total

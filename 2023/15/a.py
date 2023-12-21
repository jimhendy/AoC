def _hash(step: str) -> int:
    current_value = 0
    for character in step:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


def run(inputs: str) -> int:
    return sum(_hash(x) for x in inputs.splitlines()[0].split(","))

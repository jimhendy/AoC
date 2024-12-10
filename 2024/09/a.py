def _checksum(hard_drive: list[str]) -> int:
    total = 0
    for i, char in enumerate(hard_drive):
        if char == ".":
            break
        total += i * int(char)
    return total


def run(inputs: str) -> int:
    hard_drive = []
    is_file = True
    file_num = 0
    for n_repeats in map(int, inputs):
        char = file_num if is_file else "."
        hard_drive += [char] * n_repeats

        is_file = not is_file
        file_num += 1 if is_file else 0

    reverse_loc = len(hard_drive) - 1
    for i, char in enumerate(hard_drive):
        if char == ".":
            while hard_drive[reverse_loc] == ".":
                reverse_loc -= 1
            if reverse_loc <= i:
                break
            hard_drive[i], hard_drive[reverse_loc] = (
                hard_drive[reverse_loc],
                char,
            )
            reverse_loc -= 1

    return _checksum(hard_drive)

def _checksum(hard_drive: list[str]) -> int:
    total = 0
    for i, char in enumerate(hard_drive):
        if char != ".":
            total += i * int(char)
    return total


def run(inputs: str) -> int:
    hard_drive = []
    id_to_file_size: dict[int, int] = {}
    is_file = True
    file_num = 0
    for n_repeats in map(int, inputs):
        char = file_num if is_file else "."
        hard_drive.extend([char] * n_repeats)
        if is_file:
            id_to_file_size[file_num] = n_repeats
            file_num += 1
        is_file = not is_file

    # Find all the spaces in the drive
    free_space = [0] * len(hard_drive)
    free_space_size = 0
    for i in range(len(hard_drive) - 1, -1, -1):
        if hard_drive[i] == ".":
            free_space_size += 1
        else:
            free_space_size = 0
        free_space[i] = free_space_size

    # Defragment the drive
    location = len(hard_drive) - 1
    while location >= 0:
        file_num = hard_drive[location]

        if file_num == ".":
            location -= 1
            continue

        file_size = id_to_file_size[file_num]

        # Find the first free space from the left that can fit the file
        free_start = next(
            (i for i, size in enumerate(free_space) if size >= file_size),
            None,
        )

        if free_start is not None and free_start <= location:
            file_start = location - file_size + 1

            hard_drive[free_start : free_start + file_size] = [file_num] * file_size
            hard_drive[file_start : file_start + file_size] = ["."] * file_size
            free_space[free_start : free_start + file_size] = [0] * file_size

            # Update free space to the right
            for i in range(file_start, file_start + file_size):
                if i < len(hard_drive) - 1:
                    free_space[i] = free_space[i + 1] + 1

            # Update free space to the left
            free_loc = file_start - 1
            while free_loc >= 0 and hard_drive[free_loc] == ".":
                free_space[free_loc] = free_space[free_loc + 1] + 1
                free_loc -= 1

        location -= file_size

    return _checksum(hard_drive)

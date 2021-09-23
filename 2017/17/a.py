def do_iteration(buffer, steps, current_pos, it):
    new_pos = (current_pos + steps) % len(buffer)
    buffer.insert(new_pos + 1, it)
    return new_pos + 1


def print_buffer(buffer, pos):
    s = ""
    for i, v in enumerate(buffer):
        if i == pos:
            s += f"({v}) "
        else:
            s += f"{v} "
    print(s)


def run(inputs):
    buffer = [0]
    steps = int(inputs)
    current_pos = 0
    for it in range(1, 2018):
        current_pos = do_iteration(buffer, steps, current_pos, it)
    print_buffer(buffer, 0)
    return buffer[buffer.index(2017) + 1]

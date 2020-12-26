import os


def next_rand(i, subject_number=7):
    return (i * subject_number) % 20201227


def find_loop_size(aim):
    r = 1
    i = 0
    while r != aim:
        r = next_rand(r)
        i += 1
    return i


def run(inputs):
    card_p_key, door_p_key = map(int, inputs.split(os.linesep))

    door_loop_size = find_loop_size(door_p_key)

    r = 1
    for _ in range(door_loop_size):
        r = next_rand(r, subject_number=card_p_key)

    return r

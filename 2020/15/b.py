def run(inputs):
    most_recent = {}

    for i, n in enumerate(map(int, inputs.split(","))):
        most_recent[n] = i
        prev_num = n

    del most_recent[prev_num]

    n_turns = 30_000_000
    for turn in range(len(most_recent), n_turns - 1):
        mr = most_recent.get(prev_num, turn)
        most_recent[prev_num] = turn
        prev_num = turn - mr

    return prev_num

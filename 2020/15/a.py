def run(inputs):
    most_recent = {}

    for i, n in enumerate(inputs.split(",")):
        most_recent[int(n)] = i
        prev_num = int(n)

    del most_recent[prev_num]

    n_turns = 2020
    for turn in range(len(most_recent), n_turns - 1):

        mr = most_recent.get(prev_num)

        if mr is None:
            spoken = 0
        else:
            spoken = turn - mr

        most_recent[prev_num] = turn
        prev_num = spoken

    return prev_num

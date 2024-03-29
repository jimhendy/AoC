def run(inputs):
    floor = 0

    for step, i in enumerate(list(inputs)):
        if i == "(":
            floor += 1
        elif i == ")":
            floor -= 1
        else:
            raise NotImplementedError

        if floor == -1:
            return step + 1
    return None

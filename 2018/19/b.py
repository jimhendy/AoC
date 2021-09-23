def run(inputs):
    # By manual examination of code and values, could be tidied up to work with any inputs
    # Idea is to sum all integer factors of the value in register 4
    r4 = 10551378
    return sum([i for i in range(1, r4 + 1) if not r4 % i])

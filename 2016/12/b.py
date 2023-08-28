from assembunny import Assembunny


def run(inputs):
    a = Assembunny(inputs)
    a.registers["c"] = 1
    a()

    return a.registers["a"]

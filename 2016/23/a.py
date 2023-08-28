from assembunny import Assembunny


def run(inputs):
    a = Assembunny(inputs)
    a.registers["a"] = 7
    a()

    return a.registers["a"]

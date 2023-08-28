from assembunny import Assembunny


def run(inputs):
    a = Assembunny(inputs)
    a.registers["a"] = 12
    a()

    return a.registers["a"]

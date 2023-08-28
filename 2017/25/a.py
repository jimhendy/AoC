from turing import Turing


def run(inputs):
    machine = Turing(inputs)
    machine()

    return sum(machine.tape.values())

from assembunny import Assembunny, WrongOutputError

def run(inputs):
    i = 0
    while True:
        try:
            ab = Assembunny(inputs)
            ab.registers['a'] = i
            ab()
            break
        except WrongOutputError:
            pass
        i += 1

    return i
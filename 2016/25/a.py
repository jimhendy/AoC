from assembunny import Assembunny, WrongOutputError
from loguru import logger


def run(inputs):
    i = 0
    while True:
        try:
            logger.error(f"{i=}")
            ab = Assembunny(inputs)
            ab.registers["a"] = i
            ab()
            break
        except WrongOutputError:
            pass
        i += 1

    return i

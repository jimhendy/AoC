from register_code import RegisterCode


def run(inputs):
    rc = RegisterCode(inputs)
    rc()
    return max(rc.registers.values())

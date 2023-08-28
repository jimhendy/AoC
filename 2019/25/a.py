import itertools
import re

import intcode


def run_cmd(prog, cmd=None):
    output_len = len(prog.outputs)
    print(cmd)
    if cmd is None:
        cmd = input("Enter a command : ")
    for i in list(cmd):
        prog.analyse_intcode(ord(i))
        pass
    prog.analyse_intcode(10)
    result = "".join([chr(i) for i in prog.outputs[output_len:]])
    print(result)
    return result


def run(inputs):
    prog = intcode.Intcode(inputs)

    cmds = [
        "east",
        "south",
        "take shell",
        "north",
        "east",
        "take fuel cell",
        "west",
        "west",
        "south",
        "west",
        "take easter egg",
        "north",
        "east",
        "take space heater",
        "west",
        "south",
        "west",
        "west",
        "south",
        "west",
        "north",
        "take coin",
        "south",
        "east",
        "north",
        "take monolith",
        "west",
        "take mug",
        "north",
        "inv",
    ]

    for cmd in cmds:
        run_cmd(prog, cmd)

    things = [
        "coin",
        "mug",
        "easter egg",
        "shell",
        "fuel cell",
        "space heater",
        "monolith",
    ]
    current_inv = things[:]
    n_things = len(things)

    for n_drops in range(n_things):
        for comb in itertools.combinations(things, n_things - n_drops):
            print(comb)
            print(current_inv)

            take = [c for c in comb if c not in current_inv]
            drop = [c for c in current_inv if c not in comb]

            for c in take:
                run_cmd(prog, f"take {c}")
                current_inv.append(c)
                pass

            for c in drop:
                run_cmd(prog, f"drop {c}")
                current_inv.remove(c)
                pass

            msg = run_cmd(prog, "north")
            if 'A loud, robotic voice says "Alert! Droids on this ship are' in msg:
                print("Failure")
            else:
                reg = re.compile(r"to get in by typing (\d+) on the keypad")
                match = re.findall(reg, msg)
                return match[0]
    return None

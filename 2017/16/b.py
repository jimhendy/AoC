import numpy as np
from collections import defaultdict

def run(inputs):
    cycle = find_cycle(inputs)
    print(f'Cycle: {cycle}')
    programs = starting_positions()
    for dance in range(1_000_000_000 % cycle):
        programs = do_dance_single_cycle(programs, inputs)
    return ''.join(programs)

def starting_positions():
    return np.array(list('abcdefghijklmnop'))

def do_dance_single_cycle(programs, inputs):
    for i in inputs.split(','):
        if i[0] == 's':
            programs = spin(programs, int(i[1:]))
        elif i[0] == 'x':
            programs = exchange(programs, i[1:])
        elif i[0] == 'p':
            programs = partner(programs, i[1:])
        else:
            raise RuntimeError(f'Unknown command {i}')
    return programs    

def find_cycle(inputs):
    programs = starting_positions()
    seen = defaultdict(list)
    seen[''.join(programs)].append(0)
    for dance in range(1_000_000_000):
        programs = do_dance_single_cycle(programs, inputs)
        letters = ''.join(programs)
        if letters in seen.keys():
            return dance + 1
    return letters

def spin(programs, num):
    return np.roll(programs, num)

def exchange(programs, args):
    pos_a, pos_b = [ int(i) for i in args.split('/') ]
    return _swap_pos(programs, pos_a, pos_b)

def _swap_pos(programs, pos_a, pos_b):
    letter_b = programs[pos_b]
    programs[pos_b] = programs[pos_a]
    programs[pos_a] = letter_b
    return programs

def partner(programs, args):
    letter_a, letter_b = args.split('/')
    pos_a = np.argwhere(programs==letter_a)[0]
    pos_b = np.argwhere(programs==letter_b)[0]
    return _swap_pos(programs, pos_a, pos_b)
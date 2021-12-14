import os
from collections import deque, Counter

def step(q, alterations):
    len_before_step = len(q)
    for _ in range(len_before_step - 1):
        
        starting_pair = q[0] + q[1]
        to_insert = alterations.get(starting_pair)

        if to_insert:
            #print(f'Inserting {to_insert} between {starting_pair}')
            q.rotate(-1)
            q.appendleft(to_insert)

        q.rotate(-1)
    q.rotate(-1)

def run(inputs):
    initial, _, *alt_inputs = inputs.split(os.linesep)
    q = deque(list(initial))
    alterations = {}
    for a in alt_inputs:
        a_split = a.split(' -> ')
        if len(a_split) != 2:
            continue
        alterations[a_split[0]] = a_split[1]
    
    for i in range(40):
        print(i)
        step(q, alterations)

    counts = Counter(q)
    count_values = list(counts.values())

    return max(count_values) - min(count_values)

if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        inputs = f.read()
    print(inputs)
    print(run(inputs))
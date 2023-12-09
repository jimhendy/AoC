import queue

import intcode


def run(inputs):
    n_computers = 50
    computers = []
    for i in range(n_computers):
        p = intcode.Intcode(inputs)
        p.analyse_intcode(i)
        computers.append(p)

    queues = [queue.Queue() for _ in range(n_computers)]

    nat = {}
    ys = set()

    while True:
        all_empty = True
        for c, q in zip(computers, queues):
            if q.qsize():
                all_empty = False
                while q.qsize():
                    c.analyse_intcode(q.get())
            else:
                c.analyse_intcode(-1)

            while len(c.outputs):
                c_q = c.outputs.pop(0)
                x_q = c.outputs.pop(0)
                y_q = c.outputs.pop(0)
                if c_q == 255:
                    nat["x"] = x_q
                    nat["y"] = y_q
                else:
                    queues[c_q].put(x_q)
                    queues[c_q].put(y_q)

        if all_empty:
            if nat["y"] in ys:
                return nat["y"]
            ys.add(nat["y"])
            queues[0].put(nat["x"])
            queues[0].put(nat["y"])

    return None

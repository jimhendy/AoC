import queue

import intcode


def run(inputs):
    n_computers = 50
    computers = []
    for i in range(n_computers):
        p = intcode.Intcode(inputs)
        p.analyse_intcode(i)
        computers.append(p)
        pass

    queues = [queue.Queue() for _ in range(n_computers)]

    while True:
        for c, q in zip(computers, queues):
            if q.qsize():
                while q.qsize():
                    c.analyse_intcode(q.get())
                    pass
                pass
            else:
                c.analyse_intcode(-1)
                pass

            while len(c.outputs):
                c_q = c.outputs.pop(0)
                x_q = c.outputs.pop(0)
                y_q = c.outputs.pop(0)
                if c_q >= n_computers:
                    return y_q
                queues[c_q].put(x_q)
                queues[c_q].put(y_q)
                pass
            pass
        pass
    pass
    return None

import os
import time
from concurrent.futures import ThreadPoolExecutor

from duetcode import JumpCode


def run(inputs):

    instructions = inputs.split(os.linesep)

    p0 = JumpCode(instructions)
    p1 = JumpCode(instructions)

    p0.add_partner(p1)
    p1.add_partner(p0)

    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            print([p.is_waiting for p in (p0, p1)])
            if all([p.is_waiting for p in (p0, p1)]):
                break
            else:
                for i, p in enumerate((p0, p1)):
                    if not p.is_running:
                        print(f"Restarting {i}")
                        executor.submit(p.run)
            time.sleep(1)

    return p1.n_sends

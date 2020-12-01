from cart import Cart
import numpy as np
import os

def run(inputs):
    track = np.array([
        list(line) for line in inputs.split(os.linesep)
    ])
    carts = []
    for r, row in enumerate(track):
        for c, char in enumerate(row):
            if char.lower() in ['v','>','<','^']:
                carts.append(Cart(np.array((r,c)), track))
    
    while True:
        sorted_carts = sorted(carts)[:]
        for c in sorted_carts:
            if not c in carts:
                continue
            c.step()
            for co in carts:
                if co != c and c.loc_as_str() == co.loc_as_str():
                    carts.remove(c)
                    carts.remove(co)
                    break
        if len(carts) == 1:
            break

    c = carts[0]
    return f'{c.loc[1]},{c.loc[0]}'

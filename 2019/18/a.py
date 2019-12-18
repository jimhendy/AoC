import droid
import time
import numpy as np

def run(inputs):

    d = droid.Droid(inputs)
    d.plot(True)
    while True:
        ak = d.find_accessible_keys()
        if ak is False:
            break
        route = sorted(ak.items(), key=lambda k: len(k[1]), reverse=True)[0][1]
        for p in route:
            d.go_to(p)
            d.plot(True)
            time.sleep(0.1)
            pass
        time.sleep(0.1)
        pass
    d.plot(True)
    import code
    code.interact(local=locals())

    return 0

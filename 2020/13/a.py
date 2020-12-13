import os

def run(inputs):
    inputs = inputs.split(os.linesep)
    arrive = int(inputs[0])
    buses = [ int(i) for i in inputs[1].split(',') if i.isdigit() ]

    time = arrive
    found = False
    while True:
        for b in buses:
            if not time % b:
                found = True
                break
        if found:
            break
        time += 1
    
    return (time-arrive) * b
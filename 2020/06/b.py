import os

def run(inputs):

    total = 0
    data = None
    for line in inputs.split(os.linesep):
        
        line = line.strip()

        if not len(line):
            print(len(data))
            total += len(data)
            data = None
        else:
            if data is None:
                data = set(list(line))
            else:
                print(data, set(list(line)))
                data = data.intersection( set(list(line)) )
            
    total += len(data)

    return total
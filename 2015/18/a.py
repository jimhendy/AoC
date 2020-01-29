import os
import copy

def get_neighbours(y,x,lights):
    total = 0
    if y:
        row = lights[y-1]
        if x:
            total += row[x-1]=='#'
            pass
        total += row[x]=='#'
        if x < len(row)-1:
            total += row[x+1]=='#'
            pass
        pass
    if y < len(lights)-1:
        row = lights[y+1]
        if x:
            total += row[x-1]=='#'
            pass
        total += row[x]=='#'
        if x < len(row)-1:
            total += row[x+1]=='#'
            pass
        pass
    if x:
        total += lights[y][x-1]=='#'
        pass
    if x < len(lights[0])-1:
        total += lights[y][x+1]=='#'
        pass
    return total

def update(lights):

    orig = copy.deepcopy(lights)

    for y_i, y in enumerate(lights):
        for x_i, x in enumerate(y):
            on = x == '#'
            n_neighbours = get_neighbours(y_i, x_i, orig)
            if on:
                if n_neighbours not in [2,3]:
                    lights[y_i][x_i] = '.'
                    pass
                pass
            else:
                if n_neighbours == 3:
                    lights[y_i][x_i] = '#'
                    pass
                pass
            pass
        pass
    
    return lights
                
            
def run(inputs):

    lights = [ list(i) for i in inputs.split(os.linesep) ]
    
    for i in range(100):
        #[ print(''.join(l)) for l in lights ]
        #print()
        lights = update(lights)
        pass
    #[ print(''.join(l)) for l in lights ]
    #print()
    return sum( [ i.count('#') for i in lights ] )

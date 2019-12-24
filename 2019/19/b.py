import intcode
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

def run(inputs):
    ship_size = 100
    input_coords = [ (i,j) for i in range(20) for j in range(20) ]

    prog = intcode.Intcode(inputs)
    def test_coord(x,y):
        prog.reset()
        prog.analyse_intcode(x)
        prog.analyse_intcode(y)
        return prog.outputs[-1]

    
    outputs = []
    for i in input_coords:
        outputs.append({'x':i[0], 'y':i[1], 'o':test_coord(i[0], i[1])})
        pass

    df = pd.DataFrame(outputs)
    
    extra = []
    max_y = df.y.max()
    min_x = df[ (df.o.eq(1)) & (df.y==df.y.max()) ].x.min()
    while len(extra) < 2000:
        max_y = max_y + 1
        while not test_coord(min_x, max_y):
            min_x += 1
            pass
        extra.append( (min_x, max_y) )
        pass
    
    extra_m = []
    max_y = df.y.max()
    max_x = df[ (df.o.eq(1)) & (df.y==df.y.max()) ].x.max()
    while len(extra_m) < 2000:
        max_y = max_y + 1
        while test_coord(max_x, max_y):
            max_x += 1
            pass
        extra_m.append( (max_x, max_y) )
        pass

    df = pd.DataFrame( extra, columns=['first_x','y'] ).set_index('y')
    df = df.join( pd.DataFrame(extra_m, columns=['right_x','y']).set_index('y') ).reset_index()

    df['Diff'] = df.right_x.sub( df.first_x )
    df['MaxStartingX'] = df.right_x.sub( ship_size )
    df['FirstXShipDown'] = df.shift(-ship_size+1).first_x

    line = df[ df.MaxStartingX>=df.FirstXShipDown ].iloc[0]

    result = line.MaxStartingX * 10000 + line.y    
    print(result)
  
    return result

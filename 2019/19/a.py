import intcode
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt


def run(inputs):

    input_coords = [(i, j) for i in range(50) for j in range(50)]

    outputs = []
    for i in input_coords:
        prog = intcode.Intcode(inputs)
        prog.analyse_intcode(i[0])
        prog.analyse_intcode(i[1])
        outputs.append({"x": i[0], "y": i[1], "o": prog.outputs[-1]})
        pass

    df = pd.DataFrame(outputs)

    dfp = df.pivot_table(index="y", columns="x", values="o")
    sns.heatmap(dfp)
    plt.show()

    import code

    code.interact(local=locals())

    return len(df[df.o.ne(0)])

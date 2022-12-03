import emergency_hull_painting_robot as ehpr
import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import seaborn as sns


def run(inputs):

    robot = ehpr.EhpRobot(inputs, start_color=ehpr.Color.WHITE)
    robot.run()

    xy = np.array(
        [
            np.array([int(i) for i in k[1:-1].split()])
            for k, v in robot._colors.items()
            if v == ehpr.Color.WHITE
        ]
    ).T

    df = pd.DataFrame({"x": xy[0], "y": xy[1]})
    df["Ones"] = 1

    df = df.pivot_table(index="y", columns="x", values="Ones")
    for i in range(df.columns.max()):
        if not i in df.columns:
            df[i] = np.nan

    df = df[sorted(df.columns)]
    df.sort_index(inplace=True, ascending=False)

    sns.heatmap(df.values, cbar=False)
    plt.axis("off")
    # plt.show()

    result = input("What does it say: ")

    return result

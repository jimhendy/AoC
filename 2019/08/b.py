import common
import numpy as np
import seaborn as sns


def run(inputs):

    data = common.in_to_array(inputs)

    # 2 means transparent so replace with nans
    data = np.where(data == 2, np.nan, data)

    # Combine all the first visible layers
    output = np.full(data.shape[1:], np.nan)
    for layer in range(data.shape[0]):
        output = np.where(np.isnan(output), data[layer], output)
        pass

    # Plot the result
    sns.heatmap(output)
    # plt.show()

    result = input("What does it say: ")

    return result

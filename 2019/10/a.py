import common


def run(inputs):

    data = common.in_to_array(inputs)
    visible = common.num_visible(data)

    return visible.iloc[-1]

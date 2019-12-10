import common


def module_fuel(inputs):
    weights = common.floating_weights(inputs)
    return common.calculate_fuel(weights)


def run(inputs):
    return module_fuel(inputs).sum()

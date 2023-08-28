from status import Status


def run(inputs):
    status = Status(inputs)

    while status.my_depth <= max(status.layers.keys()):
        status.step()
    return status.severity

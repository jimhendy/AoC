import os

from layer import Layer


class Status:
    def __init__(self, inputs):
        self.inputs = inputs
        self.layers = self._get_layers()
        self.my_depth = 0
        self.my_range_position = 0
        self.severity = None

    def _get_layers(self):
        layers = dict()
        for i in self.inputs.split(os.linesep):
            depth, range_ = [int(ii.strip()) for ii in i.split(":")]
            layers[depth] = Layer(depth, range_)
        return layers

    def step(self):
        for depth, layer in self.layers.items():
            if (depth == self.my_depth) and (
                layer.scanner_range_position == self.my_range_position
            ):
                if self.severity is None:
                    self.severity = 0
                self.severity += layer.severity()
            layer.step()
        self.my_depth += 1

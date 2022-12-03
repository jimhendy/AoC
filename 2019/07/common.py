from collections import defaultdict
from enum import Enum

import numpy as np


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    pass


class optprog:
    def __init__(self, inputs):
        self.inputs = optprog.in_to_array(inputs)
        self.code = self.inputs.copy()
        self.input_signal = None
        self.address = 0
        self.param_modes = defaultdict(lambda: Mode.POSITION)
        self.optcode = None
        self.outputs = []
        self.complete = False
        pass

    @staticmethod
    def in_to_array(inputs):
        return np.array(inputs.split(",")).astype(int)

    def analyse_intcode(self, input_signal):
        self.input_signal = input_signal
        while self.analyse_instruction() is not None:
            pass
        pass

    def analyse_instruction(self):
        optcode = self.code[self.address]
        if optcode > 9:
            optcode_str = f"{optcode:05}"
            self.optcode = int(optcode_str[3:])
            self.param_modes[1] = Mode(int(optcode_str[2]))
            self.param_modes[2] = Mode(int(optcode_str[1]))
            self.param_modes[3] = Mode(int(optcode_str[0]))
            pass
        else:
            self.optcode = optcode
            self.param_modes.clear()
            pass
        return self.analyse_optcode()

    def analyse_optcode(self):
        if self.optcode == 99:
            # End of code
            self.complete = True
            return None
        func = {
            1: self.add,
            2: self.mul,
            3: self.get_input,
            4: self.get_output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
        }.get(self.optcode, None)
        if func is None:
            print(f"Address: {self.address}")
            print(f"Optcode: {self.optcode}")
            print(self.code[self.address : self.address + 4])
            raise NotImplementedError(
                f'Unexpected optcode "{self.inputs[self.address]}" at address "{self.address}"'
            )
        return func()

    def _get_value(self, mode):
        if mode == Mode.POSITION:
            return self.code[self.code[self.address]]
        elif mode == Mode.IMMEDIATE:
            return self.code[self.address]
        else:
            raise NotImplementedError
        pass

    def step(self, step=1):
        self.address += step
        pass

    def _compare(self, func):
        self.step()
        param_1 = self._get_value(self.param_modes[1])
        self.step()
        param_2 = self._get_value(self.param_modes[2])
        value = int(getattr(param_1, func)(param_2))
        self.step()
        output_address = self.code[self.address]
        self.code[output_address] = value
        self.step()
        return True

    def less_than(self):
        return self._compare("__lt__")

    def equals(self):
        return self._compare("__eq__")

    def _jump_if(self, func):
        self.step()
        value = self._get_value(self.param_modes[1])
        self.step()
        if getattr(value, func)(0):
            value = self._get_value(self.param_modes[2])
            self.address = value
            return True
            pass
        self.step()
        return True

    def jump_if_true(self):
        return self._jump_if("__ne__")

    def jump_if_false(self):
        return self._jump_if("__eq__")

    def get_input(self):
        if self.input_signal is not None:
            value = self.input_signal
            self.input_signal = None
            pass
        else:
            # No input signal - return and wait
            return None
            pass
        self.step()
        output_address = self.code[self.address]
        self.code[output_address] = value
        self.step()
        return True

    def get_output(self):
        self.step()
        value = self._get_value(mode=self.param_modes[1])
        self.outputs.append(value)
        self.step()
        return True

    def _combine(self, func):
        self.step()
        param_1 = self._get_value(mode=self.param_modes[1])
        self.step()
        param_2 = self._get_value(mode=self.param_modes[2])
        self.step()
        output_address = self.code[self.address]
        self.code[output_address] = getattr(param_1, func)(param_2)
        self.step()
        return True

    def add(self):
        return self._combine("__add__")

    def mul(self):
        return self._combine("__mul__")

import numpy as np
from enum import Enum
from collections import defaultdict


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2
    pass


class optprog():

    def __init__(self, inputs):
        self.inputs = optprog.in_to_array(inputs)
        self.code = defaultdict(int)
        for i, v in enumerate(self.inputs):
            self.code[i] = v
            pass
        self.input_signal = None
        self.address = 0
        self.param_modes = defaultdict(lambda: Mode.POSITION)
        self.optcode = None
        self.outputs = []
        self.complete = False
        self.relative_base = 0
        self._address_log = []
        pass

    @staticmethod
    def in_to_array(inputs):
        return np.array(inputs.split(',')).astype(int)

    def analyse_intcode(self, input_signal=None):
        self.input_signal = input_signal
        while self.analyse_instruction() is not None:
            pass
        pass

    def analyse_instruction(self):
        self._address_log.append(self.address)
        optcode = self.code[self.address]
        if optcode > 9:
            optcode_str = f'{optcode:05}'
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
            9: self.update_relative_base
        }.get(self.optcode, None)
        if func is None:
            print(f'Address: {self.address}')
            print(f'Optcode: {self.optcode}')
            print(self.code[self.address:self.address+4])
            raise NotImplementedError(
                f'Unexpected optcode "{self.code[self.address]}" at address "{self.address}"')
        return func()

    def _get_address(self, mode):
        assert self.address >= 0
        if mode == Mode.POSITION:
            return self.code[self.address]
        elif mode == Mode.IMMEDIATE:
            return self.address
        elif mode == Mode.RELATIVE:
            value = self._get_value(mode=Mode.IMMEDIATE)
            return self.relative_base + value
        else:
            raise NotImplementedError
        pass

    def _get_value(self, mode):
        return self.code[self._get_address(mode=mode)]

    def step(self, step=1):
        self.address += step
        pass

    def _compare(self, func):
        self.step()
        param_1 = self._get_value(self.param_modes[1])
        self.step()
        param_2 = self._get_value(self.param_modes[2])
        value = int(func(param_1, param_2))
        self.step()
        output_address = self._get_address(mode=self.param_modes[3])
        self.code[output_address] = value
        self.step()
        return True

    def less_than(self):
        return self._compare(lambda x, y: x < y)

    def equals(self):
        return self._compare(lambda x, y: x == y)

    def _jump_if(self, func):
        self.step()
        value = self._get_value(self.param_modes[1])
        self.step()
        if func(value):
            value = self._get_value(self.param_modes[2])
            self.address = value
            return True
            pass
        self.step()
        return True

    def jump_if_true(self):
        return self._jump_if(lambda x: x != 0)

    def jump_if_false(self):
        return self._jump_if(lambda x: x == 0)

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
        output_address = self._get_address(mode=self.param_modes[1])
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
        output_address = self._get_address(self.param_modes[3])
        self.code[output_address] = func(param_1, param_2)
        self.step()
        return True

    def add(self):
        return self._combine(lambda x, y: x+y)

    def mul(self):
        return self._combine(lambda x, y: x*y)

    def update_relative_base(self):
        self.step()
        value = self._get_value(mode=self.param_modes[1])
        self.step()
        self.relative_base += value
        return True

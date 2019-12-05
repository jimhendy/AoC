import numpy as np


class optprog():

    def __init__(self, inputs):

        self.inputs = optprog.in_to_array(inputs)
        self.code = self.inputs.copy()
        self.address = 0
        self.param_1_mode = None
        self.param_2_mode = None
        self.param_3_mode = None
        self.optcode = None
        self.outputs = []
        pass

    @staticmethod
    def in_to_array(inputs):
        return np.array(inputs.split(',')).astype(int)

    def analyse_intcode(self):
        while self.analyse_instruction() is not None:
            pass
        pass

    def analyse_instruction(self):
        optcode = self.code[self.address]
        # Modes: 0=position, 1=immediate
        if optcode > 9:
            optcode_str = f'{optcode:05}'
            self.optcode = int(optcode_str[3:])
            self.param_1_mode = int(optcode_str[2])
            self.param_2_mode = int(optcode_str[1])
            self.param_3_mode = int(optcode_str[0])
            pass
        else:
            self.optcode = optcode
            self.param_1_mode = 0
            self.param_2_mode = 0
            self.param_3_mode = 0
            pass
        return self.analyse_optcode()

    def analyse_optcode(self):
        if self.optcode == 99:
            # End of code
            return None
        func = {
            1: self.add,
            2: self.mul,
            3: self.get_input,
            4: self.get_output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals
        }.get(self.optcode, None)
        if func is None:
            print(f'Address: {self.address}')
            print(f'Optcode: {self.optcode}')
            print(self.code[self.address:self.address+4])
            raise NotImplementedError(
                f'Unexpected optcode "{self.inputs[self.address]}" at address "{self.address}"')
        return func()

    def _get_value(self, mode):
        if mode == 0:
            return self.code[self.code[self.address]]
        elif mode == 1:
            return self.code[self.address]
        else:
            raise NotImplementedError
        pass

    def less_than(self):
        self.address += 1
        param_1 = self._get_value(self.param_1_mode)
        self.address += 1
        param_2 = self._get_value(self.param_2_mode)
        value = int(param_1 < param_2)
        self.address += 1
        output_address = self.code[self.address]
        self.code[output_address] = value
        self.address += 1
        return True

    def equals(self):
        self.address += 1
        param_1 = self._get_value(self.param_1_mode)
        self.address += 1
        param_2 = self._get_value(self.param_2_mode)
        value = int(param_1 == param_2)
        self.address += 1
        output_address = self.code[self.address]
        self.code[output_address] = value
        self.address += 1
        return True

    
    def jump_if_true(self):
        self.address += 1
        value = self._get_value(self.param_1_mode)
        self.address += 1
        if value != 0:
            value = self._get_value(self.param_2_mode)
            self.address = value
            return True
            pass
        self.address += 1
        return True

    def jump_if_false(self):
        self.address += 1
        value = self._get_value(self.param_1_mode)
        self.address += 1
        if value == 0:
            value = self._get_value(self.param_2_mode)
            self.address = value
            return True
            pass
        self.address += 1
        return True

    def get_input(self):
        value = int(input('Please enter an input: '))
        self.address += 1
        output_address = self.code[self.address]
        self.code[output_address] = value
        self.address += 1
        return True

    def get_output(self):
        self.address += 1
        value = self._get_value(mode=self.param_1_mode)
        self.outputs.append(value)
        self.address += 1
        return True

    def add(self):
        self.address += 1
        param_1 = self._get_value(mode=self.param_1_mode)
        self.address += 1
        param_2 = self._get_value(mode=self.param_2_mode)
        self.address += 1
        output_address = self.code[self.address]
        self.code[output_address] = param_1 + param_2
        self.address += 1
        return True

    def mul(self):
        self.address += 1
        param_1 = self._get_value(mode=self.param_1_mode)
        self.address += 1
        param_2 = self._get_value(mode=self.param_2_mode)
        self.address += 1
        output_address = self.code[self.address]
        self.code[output_address] = param_1 * param_2
        self.address += 1
        return True

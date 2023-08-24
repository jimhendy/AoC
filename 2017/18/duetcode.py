import queue
import re
from collections import defaultdict


class JumpCode:

    num_codes = 0

    def __init__(self, instructions):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.registers = defaultdict(int)
        self.queue = queue.Queue()
        self.partner = None
        self.is_waiting = False
        self.is_running = False
        self.program_id = JumpCode.num_codes
        self.registers["p"] = self.program_id
        self.n_sends = 0
        JumpCode.num_codes += 1

    def add_partner(self, partner_code):
        self.partner = partner_code

    def run(self):
        self.is_running = True
        self.is_waiting = False
        while True:
            try:
                ins = self.instructions[self.instruction_pointer]
            except IndexError:
                break

            func_name, *args = ins.split()
            func = getattr(self, func_name)

            f_value = func(*args)
            if f_value is not None and f_value is False:
                # Stuck waiting
                break
            pass
        self.is_running = False

    def _get_value(self, value):
        if isinstance(value, (int, float)) or (
            isinstance(value, str) and re.match(r"^(\-?\d+)$", value)
        ):
            return int(value)
        elif isinstance(value, str):
            return self._get_value(self.registers[value])
        else:
            raise NotImplementedError(
                f'Expected value to be a string or int, found "{value}", type: "{type(value)}"'
            )

    def snd(self, x):
        freq = self._get_value(x)
        self.partner.queue.put_nowait(freq)
        self.n_sends += 1
        self.instruction_pointer += 1

    def set(self, x, y):
        self.registers[x] = self._get_value(y)
        self.instruction_pointer += 1

    def add(self, x, y):
        self.registers[x] += self._get_value(y)
        self.instruction_pointer += 1

    def mul(self, x, y):
        self.registers[x] *= self._get_value(y)
        self.instruction_pointer += 1

    def mod(self, x, y):
        self.registers[x] %= self._get_value(y)
        self.instruction_pointer += 1

    def rcv(self, x):
        self.is_waiting = True
        try:
            value = self.queue.get(timeout=1)
        except:
            return False
        self.is_waiting = False
        self.registers[x] = self._get_value(value)
        self.instruction_pointer += 1

    def jgz(self, x, y):
        if self._get_value(x) > 0:
            self.instruction_pointer += self._get_value(y)
        else:
            self.instruction_pointer += 1

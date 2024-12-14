import operator
from collections import deque
from collections.abc import Callable


class Monkey:
    def __init__(
        self,
        id: int,
        items: list[int],
        operation: Callable,
        test: Callable,
        throw_true: int,
        throw_false: int,
    ) -> None:
        self.id = id
        self.operarion = operation
        self.test = test
        self.items = deque(items)
        self.throw_true = throw_true
        self.throw_false = throw_false

        self.items_inspected = 0

    def analyse_item(self) -> tuple[int, int]:
        self.items_inspected += 1
        item = self.items.popleft()
        item = self.operarion(item) // 3
        to = self.throw_true if self.test(item) else self.throw_false
        return (item, to)

    @classmethod
    def from_init_str(cls, init_str: str) -> "Monkey":
        lines = (l.strip() for l in init_str.splitlines())
        id_ = int(next(lines).split()[-1][:-1])
        items = list(map(int, next(lines).split(":")[1].split(",")))
        operation = Monkey.extract_operation(next(lines).split("new = ")[1])
        test = Monkey.extract_test_func(next(lines).split(": ")[1])
        throw_true = int(next(lines).split(": throw to monkey ")[1])
        throw_false = int(next(lines).split(": throw to monkey ")[1])

        return cls(
            id=id_,
            items=items,
            operation=operation,
            throw_true=throw_true,
            throw_false=throw_false,
            test=test,
        )

    @staticmethod
    def extract_operation(op_str: str) -> Callable:
        components = op_str.split()
        assert len(components) == 3, f"Unexpcected {op_str=}"

        if components[1] == "+":
            op = operator.add
        elif components[1] == "*":
            op = operator.mul
        else:
            msg = f"Unexpected {components[1]=}"
            raise RuntimeError(msg)

        if components[2] == "old":
            return lambda x: op(x, x)
        return lambda x: op(x, int(components[2]))

    @staticmethod
    def extract_test_func(test_str: str) -> Callable:
        if test_str.startswith("divisible by"):
            quotient = int(test_str.split()[-1])
            return lambda x: not x % quotient
        msg = f"Unexpected {test_str=}"
        raise RuntimeError(msg)


def run(inputs):
    monkies = {}
    for init_str in inputs.split("\n\n"):
        monkey = Monkey.from_init_str(init_str)
        monkies[monkey.id] = monkey

    for _ in range(20):
        for monkey_id in range(len(monkies)):
            monkey = monkies[monkey_id]
            for item in range(len(monkey.items)):
                item, to = monkey.analyse_item()
                monkies[to].items.append(item)

    ordered = sorted(m.items_inspected for m in monkies.values())
    return ordered[-1] * ordered[-2]

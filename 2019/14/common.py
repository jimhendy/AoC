from collections import defaultdict
from functools import lru_cache

import numpy as np


class StoreEmptyException(Exception):
    pass


class NoProductionReactionException(Exception):
    pass


class Store:
    def __init__(self) -> None:
        self._store = defaultdict(int)
        self._used_store = self._store.copy()

    def is_available(self, component):
        if component.is_infinite:
            return True
        return self._store[component.element] >= component.num

    def retrieve(self, component):
        if not self.is_available(component):
            msg = f"Trying to use component {component} from the store when it is not available"
            raise StoreEmptyException(
                msg,
            )
        if component.is_infinite:
            self.add(component)
        self._store[component.element] -= component.num
        self._used_store[component.element] += component.num
        return True

    def add(self, component):
        self._store[component.element] += component.num


class Component:
    def __init__(self, c_str) -> None:
        self.c_str = c_str
        s_split = c_str.split()
        self.num = int(float(s_split[0]))
        self.element = s_split[1].strip()
        self.is_infinite = self.element == "ORE"

    def __repr__(self) -> str:
        return Component._get_repr_str(self.element, self.num)

    def __mul__(self, factor):
        return Component(Component._get_repr_str(self.element, self.num * factor))

    def __rmul__(self, factor):
        return self.__mul__(factor)

    @staticmethod
    def _get_repr_str(element, num):
        return f"{num} {element}"


class Reaction:
    def __init__(self, r_str) -> None:
        self.r_str = r_str
        s_split = r_str.split("=>")
        self.inputs = [Component(c) for c in s_split[0].split(",")]
        self.input_elements = [c.element for c in self.inputs]
        self.output = [Component(c) for c in s_split[1].split(",")]
        assert len(self.output) == 1
        self.output = self.output[0]

    def __repr__(self) -> str:
        return Reaction._get_repr_str(self.inputs, self.output)

    def __mul__(self, factor):
        return Reaction(
            Reaction._get_repr_str(
                [i * factor for i in self.inputs],
                self.output * factor,
            ),
        )

    def __rmul__(self, factor):
        return self.__mul__(factor)

    @staticmethod
    def _get_repr_str(inputs, output):
        return ", ".join([i.__repr__() for i in inputs]) + f" => {output}"

    def __call__(self, store):
        for i in self.inputs:
            if not store.is_available(i):
                msg = f"Cannot execute {self} as {i} not available in store"
                raise StoreEmptyException(
                    msg,
                )
        [store.retrieve(i) for i in self.inputs]
        store.add(self.output)


@lru_cache(maxsize=2048)
def find_reaction(reactions, element):
    possibles = [r for r in reactions if element == r.output.element]
    if len(possibles) != 1:
        ex = NoProductionReactionException if len(possibles) == 0 else Exception
        msg = f"Found {len(possibles)} reactions producing {element} : {possibles}"
        raise ex(msg)
    return possibles[0]


def run_reaction(reaction, all_reactions, store=None):
    if store is None:
        store = Store()

    while not all(store.is_available(i) for i in reaction.inputs):
        for ic in reaction.inputs:
            if not store.is_available(ic):
                input_reaction = find_reaction(all_reactions, ic.element)

                num_required_from_reactions = ic.num - store._store[ic.element]

                num_reactions_required = int(
                    np.ceil(num_required_from_reactions / input_reaction.output.num),
                )
                required_reaction = input_reaction * num_reactions_required
                run_reaction(required_reaction, all_reactions, store)
    reaction(store)
    return store

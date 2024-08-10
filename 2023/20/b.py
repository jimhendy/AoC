import math
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import IntEnum


class Pulse(IntEnum):
    low = 0
    high = 1


@dataclass
class Transmission:
    source: str
    destination: str
    pulse: Pulse


@dataclass(slots=True)
class Module(ABC):
    sources: list[str]
    destinations: list[str]
    name: str

    @abstractmethod
    def receive_pulse(
        self, transmission: Transmission
    ) -> list[Transmission] | None: ...

    def transmit_pulse(self, pulse: Pulse) -> list[Transmission]:
        return [
            Transmission(source=self.name, destination=destination, pulse=pulse)
            for destination in self.destinations
        ]


@dataclass
class FlipFlop(Module):
    state: Pulse = field(init=False, default=Pulse.low)

    def receive_pulse(self, transmission: Transmission) -> list[Transmission] | None:
        if transmission.pulse != Pulse.low:
            return
        if self.state == Pulse.low:
            self.state = Pulse.high
        else:
            self.state = Pulse.low
        return self.transmit_pulse(self.state)


@dataclass
class Conjunction(Module):
    memory: dict[str, Pulse] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.memory = {source: Pulse.low for source in self.sources}

    def receive_pulse(self, transmission: Transmission) -> list[Transmission]:
        self.memory[transmission.source] = transmission.pulse
        if all(memory == Pulse.high for memory in self.memory.values()):
            pulse = Pulse.low
        else:
            pulse = Pulse.high
        return self.transmit_pulse(pulse)


@dataclass
class Broadcaster(Module):
    def receive_pulse(self, transmission: Transmission) -> list[Transmission]:
        return self.transmit_pulse(transmission.pulse)


class Machine:
    def __init__(self, lines: list[str]) -> None:
        self.modules: dict[str, Module] = {}
        self.transmissions = deque()
        self.low_pulses = 0
        self.high_pulses = 0

        sources: dict[str, list[str]] = defaultdict(list)
        destinations: dict[str, list[str]] = defaultdict(list)
        types: dict[str, type[Module]] = {}

        for line in lines:
            source, destination = line.split(" -> ")
            if source == "broadcaster":
                name = source
                type_ = Broadcaster
            else:
                name = source[1:]
                if source[0] == "%":
                    type_ = FlipFlop
                elif source[0] == "&":
                    type_ = Conjunction
                else:
                    raise ValueError(f"Unknown module type: {source[0]}")

            dests = [d.strip() for d in destination.split(", ")]
            for d in dests:
                destinations[name].append(d)
                sources[d].append(name)
            types[name] = type_

        for name, type_ in types.items():
            self.modules[name] = type_(
                name=name, sources=sources[name], destinations=destinations[name]
            )

    def find_multiples(self) -> list[int]:
        if self.transmissions:
            raise ValueError("Transmission queue not empty")

        presses = 0
        final_module = next(
            module for module in self.modules.values() if module.destinations == ["rx"]
        )
        multiples = {s: None for s in final_module.sources}

        while True:
            presses += 1

            self.transmissions.append(
                Transmission(
                    source="button", destination="broadcaster", pulse=Pulse.low
                )
            )

            while self.transmissions:
                transmission = self.transmissions.popleft()

                if transmission.destination == final_module.name:
                    for k, v in multiples.items():
                        if (
                            v is None
                            and transmission.source == k
                            and transmission.pulse == Pulse.high
                        ):
                            multiples[k] = presses
                    if all(v is not None for v in multiples.values()):
                        return list(multiples.values())

                if transmission.destination in self.modules:
                    new_transmissions = self.modules[
                        transmission.destination
                    ].receive_pulse(transmission)
                    if new_transmissions:
                        self.transmissions.extend(new_transmissions)


def run(inputs: str) -> int:
    machine = Machine(inputs.splitlines())

    multiples = machine.find_multiples()
    print(multiples)

    return math.lcm(*multiples)

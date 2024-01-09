from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from typing import ClassVar
from collections import defaultdict, deque
import time


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
    def receive_pulse(self, transmission: Transmission) -> list[Transmission] | None:
        ...

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

            dests = destination.split(", ")
            for d in dests:
                destinations[name].append(d)
                sources[d].append(name)
            types[name] = type_

        for name, type_ in types.items():
            self.modules[name] = type_(
                name=name, sources=sources[name], destinations=destinations[name]
            )

    def press_button(self) -> None:
        low_pulses, high_pulses = 0, 0
        if self.transmissions:
            raise ValueError("Transmission queue not empty")
        self.transmissions.append(
            Transmission(source="button", destination="broadcaster", pulse=Pulse.low)
        )
        while self.transmissions:
            transmission = self.transmissions.popleft()

            if transmission.pulse == Pulse.low:
                low_pulses += 1
            else:
                high_pulses += 1

            if transmission.destination in self.modules:
                new_transmissions = self.modules[
                    transmission.destination
                ].receive_pulse(transmission)
                if new_transmissions:
                    self.transmissions.extend(new_transmissions)

        self.low_pulses += low_pulses
        self.high_pulses += high_pulses


def run(inputs: str) -> int:
    machine = Machine(inputs.splitlines())
    for _ in range(1_000):
        machine.press_button()

    return machine.low_pulses * machine.high_pulses

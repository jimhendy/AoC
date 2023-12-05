from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int


@dataclass
class RangeMapping:
    source_range: Range
    destination_range: Range


@dataclass
class Mapping:
    source: str
    destination: str

    mappings: list[RangeMapping]

    def map(self, num: int) -> int:
        for mapping in self.mappings:
            if mapping.source_range.start <= num < mapping.source_range.end:
                return mapping.destination_range.start + (
                    num - mapping.source_range.start
                )
        return num


def _extract_mappings(lines: list[str]) -> list[Mapping]:
    mappings: list[Mapping] = []

    in_map_section = False
    source_category, destionation_category = None, None
    range_mappings: list[RangeMapping] = []

    for line in lines:
        line = line.strip()

        if not line:
            if in_map_section:
                mappings.append(
                    Mapping(
                        source=source_category,
                        destination=destionation_category,
                        mappings=range_mappings,
                    ),
                )
                in_map_section = False
                source_category, destionation_category = None, None
                range_mappings = []
            continue

        if line.endswith("map:"):
            in_map_section = True
            source_category, _, destionation_category = line.split()[0].split("-")
        elif in_map_section:
            destination_num, source_num, length = list(map(int, line.split()))
            range_mappings.append(
                RangeMapping(
                    source_range=Range(start=source_num, end=source_num + length),
                    destination_range=Range(
                        start=destination_num,
                        end=destination_num + length,
                    ),
                ),
            )
        else:
            raise RuntimeError(f"Unexpected line: {line}")

    mappings.append(
        Mapping(
            source=source_category,
            destination=destionation_category,
            mappings=range_mappings,
        ),
    )

    return mappings


def _mapping_from_source(mappings: list[Mapping], source: str) -> Mapping:
    return next(mapping for mapping in mappings if mapping.source == source)


def run(inputs: str) -> int:
    lines = inputs.splitlines()

    seeds = list(map(int, lines.pop(0).split(":")[1].split()))

    mappings = _extract_mappings(lines)

    initial_source = "seed"
    final_destination = "location"

    initial_mapping = _mapping_from_source(mappings, initial_source)

    locations = {}

    for seed in seeds:
        value = seed
        source = initial_source
        mapping = initial_mapping

        while True:
            value = mapping.map(value)

            if mapping.destination == final_destination:
                locations[seed] = value
                break

            source = mapping.destination
            mapping = _mapping_from_source(mappings, source)

    return min(locations.values())

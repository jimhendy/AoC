from dataclasses import dataclass, field


class NotInRangeError(Exception):
    ...


@dataclass
class Range:
    start: int
    length: int

    end: int = field(init=False)

    def __post_init__(self):
        self.end = self.start + self.length - 1


@dataclass
class RangeMapping:
    source_range: Range
    destination_range: Range


@dataclass
class Mapping:
    source: str
    destination: str

    range_mappings: list[RangeMapping]

    def _relevant_mapping_index(self, x: int) -> int:
        for index, range_mapping in enumerate(self.range_mappings):
            if range_mapping.source_range.start <= x < range_mapping.source_range.end:
                return index

    def map(self, x: int) -> int:
        index = self._relevant_mapping_index(x)
        if index is not None:
            range_mapping = self.range_mappings[index]
            return range_mapping.destination_range.start + (
                x - range_mapping.source_range.start
            )
        return x

    def range_headroom(self, x: int) -> tuple[int, int]:
        index = self._relevant_mapping_index(x)
        if index is not None:
            range_mapping = self.range_mappings[index]
            return range_mapping.source_range.end - x
        raise NotInRangeError

    def next_relevant_range_mapping(self, x: int) -> RangeMapping:
        if self._relevant_mapping_index(x) is not None:
            raise RuntimeError("Already in a range")
        distance_to_start = {
            range_mapping.source_range.start - x: range_mapping
            for range_mapping in self.range_mappings
        }
        positive_distances = {k: v for k, v in distance_to_start.items() if k > 0}

        if not positive_distances:
            raise NotInRangeError

        min_distance = min(positive_distances.keys())
        return positive_distances[min_distance]


def _extract_mappings(lines: list[str]) -> list[Mapping]:
    mappings: list[Mapping] = []

    in_map_section = False
    cat_source, cat_dest = None, None
    range_mappings: list[RangeMapping] = []

    for line in lines:
        line = line.strip()

        if not line:
            if in_map_section:
                mappings.append(
                    Mapping(
                        source=cat_source,
                        destination=cat_dest,
                        range_mappings=range_mappings,
                    ),
                )
                in_map_section = False
                cat_source, cat_dest = None, None
                range_mappings = []
            continue

        if line.endswith("map:"):
            in_map_section = True
            cat_source, _, cat_dest = line.split()[0].split("-")
        elif in_map_section:
            num_dest, num_source, length = list(map(int, line.split()))
            range_mappings.append(
                RangeMapping(
                    source_range=Range(start=num_source, length=length),
                    destination_range=Range(start=num_dest, length=length),
                ),
            )
        else:
            raise RuntimeError(f"Unexpected line: {line}")

    mappings.append(
        Mapping(
            source=cat_source,
            destination=cat_dest,
            range_mappings=range_mappings,
        ),
    )

    return mappings


def _mapping_from_source(mappings: list[Mapping], source: str) -> Mapping:
    return next(mapping for mapping in mappings if mapping.source == source)


def destination_ranges(range_: Range, mapping: Mapping) -> list[Range]:
    dest_ranges = []

    x = range_.start
    while True:
        y = mapping.map(x)
        try:
            length = mapping.range_headroom(x)
        except NotInRangeError:
            try:
                next_range_mapping = mapping.next_relevant_range_mapping(x)
                length = next_range_mapping.source_range.start - x
            except NotInRangeError:
                # No next range, just y=x
                length = range_.end + 3

        length = min(length, range_.end - x + 1)
        dest_ranges.append(Range(start=y, length=length))
        x += length

        if x >= range_.end:
            break

    return dest_ranges


def run(inputs: str) -> int:
    lines = inputs.splitlines()

    seeds = list(map(int, lines.pop(0).split(":")[1].split()))
    seed_ranges = [
        Range(start=seeds[i], length=seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]

    mappings = _extract_mappings(lines)

    source = "seed"
    current_ranges = seed_ranges

    while True:
        current_mapping = _mapping_from_source(mappings, source)
        next_ranges = []

        for range_ in current_ranges:
            next_ranges.extend(
                destination_ranges(
                    range_,
                    current_mapping,
                ),
            )

        source = current_mapping.destination
        current_ranges = next_ranges

        if source == "location":
            break

    return min(range_.start for range_ in current_ranges)

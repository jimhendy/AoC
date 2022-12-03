import itertools


def chunked_iterable(iterable, size):
    it = iter(iterable)
    while True:
        if chunk := tuple(itertools.islice(it, size)):
            yield chunk
        else:
            break


def priority(character: str) -> int:
    return ord(character) - (96 if character.islower() else 38)


def run(inputs):
    return sum(
        priority(set.intersection(*(set(rucksack) for rucksack in group)).pop())
        for group in chunked_iterable(inputs.splitlines(), 3)
    )

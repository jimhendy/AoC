import re
from collections import Counter


def run(inputs):

    reg = re.compile("([a-z\-]+)\-(\d+)\[([a-z]+)\]")

    total = 0

    for match in reg.findall(inputs):
        name = Counter(match[0].replace("-", ""))
        sector_id = int(match[1])
        checksum = match[2]

        counts = sorted(name.items(), key=lambda x: (-x[1], x[0]))

        my_checksum = "".join([i[0] for i in counts[:5]])
        if checksum == my_checksum:
            total += sector_id

    return total

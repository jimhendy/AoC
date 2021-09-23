import os
import re


def run(inputs):

    data = "".join(inputs.split(os.linesep))

    marker_reg = re.compile("\((\d+)x(\d+)\)")
    prev_end_pos = 0

    output = ""

    for match in marker_reg.finditer(data):

        start, end = match.span()
        if start < prev_end_pos:
            # Still inside the previous marker
            continue

        # fill anything missing
        output += data[prev_end_pos:start]

        n_chars, repeats = list(map(int, match.groups()))
        prev_end_pos = end + n_chars
        chars = data[end:prev_end_pos]
        output += chars * repeats

    output += data[prev_end_pos:]
    return len(output)

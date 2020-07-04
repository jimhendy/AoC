import re

def run(inputs):

    result = sum(
        [
            int(m[0]) * len(m[1])
            for m in re.findall(r'(\d)(\1+)', inputs)
        ]
    )

    # Ensure we have considered the circulare case
    if inputs[-1] == inputs[0]:
        result += int(inputs[0])
    return result
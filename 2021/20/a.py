import os

from tools.number_conversion import binary_to_decimal

# coords = (y, x)

STEPS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))
ON = "1"
OFF = "0"


def enhance(pixels: dict, iea: str, default: str) -> dict:
    output = {}

    xs = [k[1] for k in pixels]
    ys = [k[0] for k in pixels]

    delta = 2
    min_x = min(xs) - delta
    max_x = max(xs) + delta
    min_y = min(ys) - delta
    max_y = max(ys) + delta

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            binary = []
            for step in STEPS:
                c = (y + step[0], x + step[1])
                binary.append(pixels.get(c, default))

            decimal_num = binary_to_decimal(binary)
            output[(y, x)] = iea[decimal_num]
    return output


def run(inputs: str) -> int:
    inputs = inputs.replace("#", ON).replace(".", OFF)

    iea, input_image = inputs.split(os.linesep * 2)
    input_image = input_image.split(os.linesep)
    pixels = {}
    for row_num, row in enumerate(input_image):
        for col_num, character in enumerate(row):
            pixels[(row_num, col_num)] = character

    odd_default = iea[0]
    even_default = OFF if odd_default == OFF else iea[sum(2**i for i in range(9))]

    for i in range(2):
        pixels = enhance(
            pixels,
            iea,
            default=OFF if not i else (odd_default if i % 2 else even_default),
        )

    return len([v for v in pixels.values() if v == "1"])

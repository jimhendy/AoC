DIGITS = {"=": -2, "-": -1}
SNAFU_BASE = 5


def _snafu_digit(digit: str) -> int:
    return int(DIGITS.get(digit, digit))


def snafu_to_decimal(snafu: str) -> int:
    return sum(
        SNAFU_BASE**power * _snafu_digit(digit)
        for power, digit in enumerate(snafu[::-1])
    )


def invoke_higher_power(output: list[str], power: int) -> None:
    if len(output) <= power + 1:
        output.append("0")

    match output[power + 1]:
        case "=":
            result = "-"
        case "-":
            result = "0"
        case _:
            result = str(int(output[power + 1]) + 1)
    output[power + 1] = result


def deciaml_to_snafu(decimal: int) -> str:
    simple_base = []

    while decimal:
        simple_base.append(decimal % SNAFU_BASE)
        decimal //= SNAFU_BASE

    # In SNAFU_BASE as a list of strings, starting from SNAFU_BASE^0 and increasing powers
    output = list(map(str, simple_base))

    for power in range(len(output)):
        char = output[power]
        match char:
            case "3":
                output[power] = "="
                invoke_higher_power(output, power)
            case "4":
                output[power] = "-"
                invoke_higher_power(output, power)
            case "5":
                output[power] = "0"
                invoke_higher_power(output, power)
            case _:
                ...

    return "".join(output[::-1])


def run(inputs: str) -> int:
    total = sum(map(snafu_to_decimal, inputs.splitlines()))
    print(total)
    return deciaml_to_snafu(total)

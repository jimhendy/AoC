import os
import re

bracket_reg = re.compile(r"(\([^\(]+?\))")
int_reg = re.compile(r"(\d+)")
operator_reg = re.compile(r"([\*\+])")


def evaluate_first_bracket_term(line):
    for match in bracket_reg.finditer(line):
        line = (
            line[: match.start()] + evaluate_term(match.group()) + line[match.end() :]
        )
        break
    return line


def evaluate_term(term):
    ints = list(map(int, int_reg.findall(term)))
    ops = operator_reg.findall(term)
    result = ints[0]
    for i, o in zip(ints[1:], ops):
        if o == "+":
            result += i
        elif o == "*":
            result *= i
        else:
            raise NotImplementedError
    return str(result)


def run(inputs):
    lines = inputs.split(os.linesep)
    results = []
    for line in lines:
        while "(" in line:
            line = evaluate_first_bracket_term(line)
        results.append(evaluate_term(line))
    return sum(map(int, results))
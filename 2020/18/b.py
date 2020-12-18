import os
import re

bracket_reg = re.compile(r"(\([^\(]+?\))")
int_reg = re.compile(r"(\d+)")
addition_reg = re.compile(r"(\d+) \+ (\d+)")
multiplication_reg = re.compile(r"(\d+) \* (\d+)")


def evaluate_first_bracket_term(line):
    for match in bracket_reg.finditer(line):
        line = (
            line[: match.start()]
            + evaluate_term(match.group()).lstrip("(").rstrip(")")
            + line[match.end() :]
        )
        break  # Looks daft to break every time but the match.start()/end() indices refer to the original string so need to "reindex" for each replacement
    return line


def evaluate_term(line):
    line = evaluate_operator(line, "+", addition_reg, lambda x, y: x + y)
    line = evaluate_operator(line, "*", multiplication_reg, lambda x, y: x * y)
    return line


def evaluate_operator(line, op, reg, func):
    while op in line:
        for match in reg.finditer(line):
            result = func(int(match[1]), int(match[2]))
            line = line[: match.start()] + str(result) + line[match.end() :]
            break
    return line


def run(inputs):
    lines = inputs.split(os.linesep)
    results = []
    for line in lines:
        while "(" in line:
            line = evaluate_first_bracket_term(line)
        results.append(evaluate_term(line))
    return sum(map(int, results))
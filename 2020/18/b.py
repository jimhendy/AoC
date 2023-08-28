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


def evaluate_term(term):
    term = evaluate_operator(term, "+", addition_reg, lambda x, y: x + y)
    return evaluate_operator(term, "*", multiplication_reg, lambda x, y: x * y)


def evaluate_operator(term, op, reg, func):
    while op in term:
        for match in reg.finditer(term):
            result = func(int(match[1]), int(match[2]))
            term = term[: match.start()] + str(result) + term[match.end() :]
            break
    return term


def run(inputs):
    lines = inputs.split(os.linesep)
    results = []
    for line in lines:
        while "(" in line:
            line = evaluate_first_bracket_term(line)
        results.append(evaluate_term(line))
    return sum(map(int, results))

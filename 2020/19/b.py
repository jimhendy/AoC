import os
import re


def run(inputs):
    rules, messages = inputs.split(os.linesep * 2)
    rules = {
        r.split(":")[0]: "(?: " + r.split(":")[1].replace('"', "") + " )"
        for r in rules.split(os.linesep)
    }
    messages = messages.split(os.linesep)

    while any(
        character.isdigit() for rule_reg in rules.values() for character in rule_reg
    ):
        for rule_num, rule_reg in rules.items():
            for sub_rule_num in re.findall(r"(\d+)", rule_reg):
                rules[rule_num] = re.sub(
                    f" {sub_rule_num} ",
                    " " + rules[sub_rule_num] + " ",
                    rules[rule_num],
                )

    for k, v in rules.items():
        rules[k] = v.replace(" ", "")

    # 0 = 8 11
    # Match 42 31 from centre
    # Any number of 42s on the left

    reg = re.compile(
        "^(" + rules["42"] + ")(" + rules["42"] + ")+(" + rules["31"] + ")+$",
    )
    reg_11_rep = re.compile(
        "^(?:"
        + rules["42"]
        + ")+"
        + "("
        + rules["42"]
        + rules["31"]
        + ")(?:"
        + rules["31"]
        + ")*$",
    )
    reg_8 = re.compile("^(" + rules["42"] + ")+$")

    total = 0
    for m in messages:
        if not reg.search(m):
            # Test if this line roughly matches the desired pattern
            continue
        while reg_11_rep.match(m):
            # Remove all inner couples of 42 + 31
            # match indicies refer to input m so as we are altering m in each iteration must retest every time (I think)
            for match in reg_11_rep.finditer(m):
                m = m[: match.start(1)] + m[match.end(1) :]
                break
        if not reg_8.search(m):
            # Ensure we still have at least one 42 at the start
            continue
        total += 1

    return total

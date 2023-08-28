import os
import re


def run(inputs):
    rules, messages = inputs.split(os.linesep * 2)
    rules = {
        r.split(":")[0]: "( " + r.split(":")[1].replace('"', "") + " )"
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
        rules[k] = "^" + v.replace(" ", "") + "$"

    total = 0
    for m in messages:
        if re.search(rules["0"], m):
            total += 1

    return total

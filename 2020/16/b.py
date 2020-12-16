import os
import re

import numpy as np
import pandas as pd


def run(inputs):

    rules, my_ticket, tickets = extract_data(inputs)
    valid_tickets = find_valid_tickets(rules, tickets)
    rule_index = find_rules_index(rules, valid_tickets)

    nums = []
    for rule_name, index in rule_index.items():
        if rule_name.startswith("departure"):
            nums.append(my_ticket[index])

    return np.product(nums)


def extract_data(inputs):
    rules = {}
    my_ticket = None
    tickets = []
    for line in inputs.split(os.linesep):
        if ":" in line and "or" in line:
            rule_name = line.split(":")[0].strip()
            nums = list(map(int, re.findall(r"(\d+)", line)))
            rules[rule_name] = nums
        else:
            nums = re.findall(r"(\d+)", line)
            if not len(nums):
                continue
            if my_ticket is None:
                my_ticket = list(map(int, nums))
            else:
                tickets.append(list(map(int, nums)))
    return rules, my_ticket, tickets


def find_valid_tickets(rules, tickets):
    valid_tickets = []
    for ticket in tickets:
        valid_ticket = True
        for num in ticket:
            valid_num = False
            for rule_name, rule in rules.items():
                if rule[0] <= num <= rule[1] or rule[2] <= num <= rule[3]:
                    valid_num = True
                    break
            if not valid_num:
                valid_ticket = False
                break
        if valid_ticket:
            valid_tickets.append(ticket)
    return valid_tickets


def find_rules_index(rules, valid_tickets):
    data = []
    for ticket in valid_tickets:
        for num_i, num in enumerate(ticket):
            for rule_name, rule in rules.items():
                valid = rule[0] <= num <= rule[1] or rule[2] <= num <= rule[3]
                data.append(
                    {"Num_i": num_i, "RuleName": rule_name, "Valid": int(valid)}
                )
    df = pd.DataFrame(data).pivot_table(
        index="RuleName", columns="Num_i", values="Valid", aggfunc="mean"
    )
    df[df.ne(1)] = 0
    df = df.astype(int)

    rule_index = {}
    while len(rule_index) != len(rules):
        cols = [c for c in df.columns if not c in rule_index.values()]
        df_s = df[cols].sum(axis=1)
        for rule_name, _ in df_s[df_s.eq(1)].iteritems():
            rule_index[rule_name] = (
                df[cols].loc[rule_name].replace(0, np.nan).dropna().index[0]
            )

    return rule_index

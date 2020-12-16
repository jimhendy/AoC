import os
import re

def run(inputs):
    rules = {}
    my_ticket = None
    tickets = []
    for line in inputs.split(os.linesep):
        if ':' in line and 'or' in line:
            rule_name = line.split(':')[0].strip()
            nums = list(map(int, re.findall(r'(\d+)', line)))
            rules[rule_name] = nums
        else:
            nums = re.findall(r'(\d+)', line)
            if not len(nums):
                continue
            if my_ticket is None:
                my_ticket = list(map(int, nums))
            else:
                tickets.append(list(map(int, nums)))

    error_rate = 0
    for ticket in tickets:
        for num in ticket:
            valid_num = False
            for rule_name, rule in rules.items():
                if rule[0] <= num <= rule[1] or rule[2] <= num <= rule[3]:
                    valid_num = True
                    break
            if not valid_num:
                error_rate += num

    return error_rate    

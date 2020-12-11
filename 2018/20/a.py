import networkx as nx
import re

def extract_sub_options(txt):
    output = ['']
    level = 0
    for c in txt:
        if c == '(':
            level += 1

        if not level:
            for i,o in enumerate(output):
                output[i] = o + c
        elif 




        if level == ')':
            level -= 1



'''

def extract_sub_options(txt, base=""):
    if len(txt) and txt[0] == '(':
        print(txt)
        txt = txt.lstrip('(').rstrip(')')
    if not '|' in txt:
        return [ base + txt ]
    print(txt)
    output = []
    level = 0
    this_output = ""
    for c in txt:

        if c == "(":
            level += 1
        elif c == ")":
            level -= 1
        
        if not level:
            if c == "|":
                print(f'- {this_output}')
                output.extend(extract_sub_options(this_output, base))
                this_output = ""
            elif c not in ['(',')']:
                base += c
        else:
            this_output += c

    if len(this_output):
        print(f'Final = {this_output}')
        output.extend(extract_sub_options(this_output, base))
    return output
'''

def run(inputs):
    inputs = "^ENWWW(NEEE|SSE(EE|N))$"
    inputs = inputs.strip().rstrip("$").lstrip("^")

    print(extract_sub_options(inputs))


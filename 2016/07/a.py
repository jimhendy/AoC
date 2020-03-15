import re
import os

def run(inputs):

    abba_reg = '(?P<a>[a-z])(?P<b>(?!(?P=a))[a-z])(?P=b)(?P=a)'
    
    good_tls = re.compile(r'(^|\])[a-z]*' + abba_reg)
    bad_tls = re.compile(r'\[[a-z]*' + abba_reg + '[a-z]*\]')

    total = 0
    for line in inputs.split(os.linesep):
        if len(good_tls.findall(line)) and not len(bad_tls.findall(line)):
            total += 1

    return total

import os
import re
from collections import Counter, defaultdict

ORD_A = ord('a')
ORD_Z = ord('z')
ORD_SPAN = ORD_Z - ORD_A + 1

def cipher(key, shift):
    result = ord(key) + (shift % ORD_SPAN)
    if result > ORD_Z:
        result -= ORD_SPAN
    return chr(result)
    
def run(inputs):

    reg = re.compile('([a-z\-]+)\-(\d+)\[([a-z]+)\]')

    results = defaultdict(list)
    
    for match in reg.findall( inputs ):
        name = Counter(match[0].replace('-',''))
        sector_id = int(match[1])
        checksum = match[2]

        counts = sorted(
            name.items(),
            key=lambda x : (-x[1],x[0])
        )

        my_checksum = ''.join([ i[0] for i in counts[:5] ])
        if checksum != my_checksum:
            continue

        deciphered = ' '.join([
            ''.join([
                cipher(character, sector_id)
                for character in word
            ])
            for word in match[0].split('-')
        ])
            
        if 'north' in deciphered:
            results[sector_id].append(deciphered)

    #print(results)

    assert len(results) == 1

    return list(results.keys())[0]

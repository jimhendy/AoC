import re
import hashlib

REG_3 = re.compile(r'(?P<char>.)(?P=char){2}')


def get_hash(s):
    return hashlib.md5(s.encode()).hexdigest().lower()

def get_n_hashes(s, n):
    _s = s
    for _ in range(n):
        _s = get_hash(_s)
    return _s

def triples(s):
    return [
        match[0]
        for match in REG_3.findall(s)
    ]

def run(salt):
    index = -1
    possibles = {}
    keys = []
    while len(keys) < 64:
        index += 1
    
        test_str = f'{salt}{index}'
        str_hash = get_n_hashes(test_str, 2017)
        trips = triples(str_hash)
        
        if len(trips):
            print(f'Triple {index}')
            possibles[index] = trips[0]
        else:
            # If not at least a triple not gonna be a 5
            continue

        to_delete = []
        for k,v in sorted(possibles.items(), key=lambda x : x[0]):
            
            if k == index:
                continue

            if k <= index - 1000:
                to_delete.append(k)
            else:
                for trip_char in v:
                    if trip_char * 5 in str_hash:
                        keys.append((k,index))
                        print(f'Key {k, index}')
                        to_delete.append(k)
        for k in to_delete:
            possibles.pop(k)
        
    return keys[63][0]
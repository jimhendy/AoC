import hashlib
import re

REG_3 = re.compile(r"(?P<char>.)(?P=char){2}")


def get_hash(s):
    return hashlib.md5(s.encode()).hexdigest().lower()


def triples(s):
    return [match[0] for match in REG_3.findall(s)]


def run(salt):
    index = -1
    possibles = {}
    keys = []
    while len(keys) < 64:
        index += 1

        test_str = f"{salt}{index}"
        str_hash = get_hash(test_str)
        trips = triples(str_hash)

        if len(trips):
            possibles[index] = trips[0]
        else:
            # If not at least a triple not gonna be a 5
            continue

        to_delete = []
        for k, v in possibles.items():
            if k == index:
                continue

            if k < index - 1000:
                to_delete.append(k)
            else:
                for trip_char in v:
                    if trip_char * 5 in str_hash:
                        keys.append((k, index))
                        to_delete.append(k)
        for k in to_delete:
            possibles.pop(k)

    return keys[63][0]

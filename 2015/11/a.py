import re

def increment(password):
    if password[-1] == 'z':
        return increment(password[:-1]) + ['a']
    else:
        return password[:-1] + [chr(ord(password[-1])+1)]
    pass

def is_increasing(password):
    nums = list(map(ord, password) )
    l = 0
    for i,j in zip(nums[:-1], nums[1:]):
        if j-i == 1:
            l += 1
            if l == 2:
                return True
        else:
            l = 0
            pass
        pass
    return False

def is_pairs(password):
    p = ''.join(password)
    matches = re.findall(r'(\D)(\1)', p)
    if len( set([m[0] for m in matches]) ) < 2:
        return False
    return True

def is_good_chars(password):
    return not any([i in password for i in ['i','o','l']])
    
def run(inputs):
    password = list(inputs)
    while True:
        increasing = is_increasing(password)
        good_chars = is_good_chars(password)
        pairs = is_pairs(password)
        if increasing and good_chars and pairs:
            return ''.join(password)
        password = increment(password)
        pass

    pass

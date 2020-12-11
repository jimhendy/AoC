def extract_sub_options(txt):

    if not '(' in txt:
        return txt.split('|')

    output = ['']
    level  = 0

    bracket_start, bracket_end = None, None

    for i, ci in enumerate(txt):
        
        if ci == '(':
            level += 1
            if level == 1:
                bracket_start = i
        

        if not level:
            for i,o in enumerate(output):
                output[i] = o + ci
        
        if ci == ')':
            level -= 1
            if level == 0:
                bracket_end = i
    
        if bracket_start is not None and bracket_end is not None and not level:
            sub_options = extract_sub_options(
                txt[bracket_start+1:bracket_end]
            )
            print(sub_options)
            for i,o in enumerate(output):
                for j, so in enumerate(sub_options):
                    if not j:
                        output[i] = o + so
                    else:
                        output.append(o+so)
            bracket_start = None
            bracket_end = None
    
    return output



def run(inputs):
    inputs = "^E(N|S(E|W))N$"
    inputs = '^N(E|W)$'
    inputs = inputs.strip().rstrip("$").lstrip("^")

    print(extract_sub_options(inputs))


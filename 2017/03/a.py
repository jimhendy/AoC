def run(inputs):

    target = int(inputs)

    upper_square_root = 1
    while True:
        upper_sqaure = upper_square_root ** 2
        if upper_sqaure > target:
            break
        upper_square_root += 2

    lower_square_root = upper_square_root - 2
    lower_square = lower_square_root ** 2

    lower_square_coord = ( lower_square_root - 1 ) / 2
    lower_square_coords = [lower_square_coord, lower_square_coord]

    if target == lower_square:
        return sum(lower_square_coords)

    current_value = lower_square
    current_coord = [ i + 1 for i in lower_square_coords]
    steps = {
        0 : [ 0, -1],
        1 : [-1,  0],
        2 : [ 0, +1], 
        3 : [+1,  0]
    }
    while current_value != target:
        current_value += 1
        step = steps[ (current_value-lower_square-1) // (lower_square_root+1) ]
        current_coord = [ c + s for c,s in zip(current_coord, step)]
        
    return sum([abs(i) for i in current_coord])


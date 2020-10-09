import numba

@numba.njit
def spinlock(steps, n_iterations):
    
    # Start from [ 0 (1) ]
    second_number = 1
    current_pos = 1

    for new_num in range(2, n_iterations+1):
        # buffer_length before insertion == new_num
        new_pos = ( current_pos + steps ) % new_num
        if not new_pos:
            second_number = new_num
        current_pos = new_pos + 1
    return second_number

def run(inputs):
    n = 50_000_000
    steps = int(inputs)

    return spinlock(steps, n)

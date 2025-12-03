N = 12

def run(input: str) -> int:
    total = 0
    for line in input.splitlines():
        nums = []
        max_pos = 0

        for i in range(N):

            sub_line = line[max_pos: -N + i + 1 or None]

            max_n = max(sub_line)            
            max_pos = line.index(max_n, max_pos) + 1
            nums.append(max_n)

        total += int("".join(nums))

    return total

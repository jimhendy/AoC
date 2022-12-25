def run(inputs):
    nums = list(enumerate(map(int, inputs.splitlines())))
    n_nums = len(nums)
    for i in range(n_nums):
        current_loc = next(loc for loc, value in enumerate(nums) if value[0] == i)
        value = nums.pop(current_loc)
        new_loc = (current_loc + value[1]) % (n_nums - 1)
        nums.insert(new_loc, value)

    zero_loc = next(loc for loc, value in enumerate(nums) if value[1] == 0)
    total = 0
    for i in range(1, 4):
        loc = (zero_loc + (i * 1_000)) % n_nums
        total += nums[loc][1]

    return total

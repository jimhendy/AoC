import itertools
KEY = 811589153


def run(inputs):
    nums = list(enumerate(map(int, inputs.splitlines())))
    nums = [(v[0], v[1] * KEY) for v in nums]
    n_nums = len(nums)

    for _, i in itertools.product(range(10), range(n_nums)):
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

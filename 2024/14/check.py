num_1 = 86
num_2 = 154

step_1 = 101
step_2 = 103

while num_1 != num_2:
    if num_1 < num_2:
        num_1 += step_1
    else:
        num_2 += step_2

print(num_1)

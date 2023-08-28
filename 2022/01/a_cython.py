# with open(cython_file, "w") as f:
#     f.write(
#         r"""def run(int[:] input_bytes):
#     cdef int new_line_char = 10
#     cdef int zero_char = 48
#     cdef int curr_max = 0
#     cdef int num = 0
#     cdef int sum = 0
#     cdef int digit = 0
#     cdef int byte = 0
#     for i in range(input_bytes.shape[0]):

#         if input_bytes[i] != new_line_char:
#     if curr_max > sum:
#     return sum"""


# with open(setup_file, "w") as f:
#     f.write(
#         f"""

# setup(
# """

# subprocess.check_call(


# def run(inputs):
#     return cheat_1.run(inputs.encode("ascii")))

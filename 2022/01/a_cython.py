# import os
# import pathlib
# import subprocess
# import sys

# here = pathlib.Path(__file__).parent
# cython_file = here / "cheat_1.pyx"
# setup_file = here / "setup.py"


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
#             digit = input_bytes[i] - zero_char
#             num = num * 10 + digit
#         elif num == 0:
#             curr_max = max(sum, curr_max)
#             sum = 0
#         else:
#             sum += num
#             num = 0
#     sum += num
#     if curr_max > sum:
#         return curr_max
#     return sum"""
#     )


# with open(setup_file, "w") as f:
#     f.write(
#         f"""
# from setuptools import setup
# from Cython.Build import cythonize

# setup(
#     ext_modules = cythonize("{cython_file}", annotate=True)
# )
# """
#     )

# subprocess.check_call(
#     f"cd {here}; "
#     f"{sys.executable} -m pip install --target={here} cython; "
#     f"{sys.executable} {setup_file} build_ext --inplace",
#     shell=True,
# )


# import cheat_1
# import numpy as np


# def run(inputs):
#     return cheat_1.run(inputs.encode("ascii")))

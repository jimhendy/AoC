import os
import pathlib
import subprocess
import sys

here = pathlib.Path(__file__).parent
cython_file = here / "cheat.pyx"
setup_file = here / "setup.py"

with open(cython_file, "w") as f:
    f.write(
        r"""def run(input_data):
    return max(sum(map(int, e.splitlines())) for e in input_data.split("\n\n"))
"""
    )


with open(setup_file, "w") as f:
    f.write(
        f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("{cython_file}")
)
"""
    )

subprocess.check_call(
    f"{sys.executable} -m pip install --target={here} cython; "
    f"{sys.executable} {setup_file} build_ext --inplace",
    shell=True,
)


import cheat


def run(inputs):
    return cheat.run(inputs)

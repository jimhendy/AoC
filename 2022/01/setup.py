from Cython.Build import cythonize
from setuptools import setup

setup(ext_modules=cythonize("/home/jim/Projects/AoC/2022/01/cheat.pyx"))

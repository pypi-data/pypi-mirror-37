from setuptools import setup
from setuptools.extension import Extension
#from setuptools.command.build_ext import build_ext as _build_ext
from Cython.Build import cythonize

import numpy as np
my_include_dirs = [np.get_include()]

#extensions = [
#        Extension("awe2d_test", ["awe2d_test.pyx"],
#                  include_dirs=my_include_dirs)
#        ]

extensions = [
        Extension("generate_pml_coeff", ["generate_pml_coeff.pyx"],
                  include_dirs=my_include_dirs,
                  extra_compile_args=['-fopenmp', '-O2', '-mavx'],
                  extra_link_args=['-fopenmp',],
                  libraries=[]),
        Extension("awe2d", ["awe2d.pyx"],
                  include_dirs=my_include_dirs,
                  extra_compile_args=['-fopenmp', '-O2', '-mavx'],
                  extra_link_args=['-fopenmp',],
                  libraries=[])
        ]

setup(
      ext_modules = cythonize(extensions)
      )
# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages
import numpy
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension(name="pmi_cython", sources=["DocumentFeatureSelection/pmi/pmi_cython.pyx"])],
    include_dirs = [numpy.get_include()]
)
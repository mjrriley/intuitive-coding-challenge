from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension

import os
import sys
import setuptools
import pybind11

#cpp_args = ['-std=c++11', '-stdlib=libc++']
#
#ext_modules = [
#    Extension(
#    'embedded_interface',
#        ['src/embedded.cpp', 'src/main.cpp'],
#        include_dirs=[pybind11.get_include(), 'include'],
#    language='c++',
#    extra_compile_args = cpp_args,
#    ),
#]

SRC_FILES = [ 
    'src/embedded.cpp', 
    'src/main.cpp'
]

INCLUDE_DIRS = [ 
    pybind11.get_include(), 
    'include' 
]

ext_modules = [
    Pybind11Extension(
        "embeddedPy",
        sorted(SRC_FILES),
        include_dirs=INCLUDE_DIRS,
        cxx_std=14
    ),
]

setup(
    name="embeddedPy",
    version='0.0.1',
    author="Matthew Riley",
    author_email="inbox@matthewriley.dev",
    description="Python interface to embedded.cpp",
    ext_modules=ext_modules,
    packages = ['app']
)

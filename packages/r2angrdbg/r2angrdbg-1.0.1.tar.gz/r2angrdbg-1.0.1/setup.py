#!/usr/bin/env python

__author__ = "Andrea Fioraldi"
__copyright__ = "Copyright 2017, Andrea Fioraldi"
__license__ = "BSD 2-Clause"
__email__ = "andreafioraldi@gmail.com"

from setuptools import setup

VER = "1.0.1"

setup(
    name='r2angrdbg',
    version=VER,
    license=__license__,
    description='Use angr inside the radare2 debugger. Create an angr state from the current debugger state. ',
    author=__author__,
    author_email=__email__,
    url='https://github.com/andreafioraldi/r2angrdbg',
    download_url = 'https://github.com/andreafioraldi/r2angrdbg/archive/' + VER + '.tar.gz',
    package_dir={'r2angrdbg': 'r2angrdbg'},
    packages=['r2angrdbg'],
    install_requires=['angrdbg'],
)

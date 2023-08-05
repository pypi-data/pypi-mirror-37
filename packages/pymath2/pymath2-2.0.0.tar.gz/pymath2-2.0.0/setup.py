#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='pymath2',
    version='2.0.0',
    packages=find_packages(exclude=('tests',)),
    scripts=['scripts/pymath'],
    description='Easy calculations on the command line with Python',
    url='https://github.com/cjbassi/pymath',
)

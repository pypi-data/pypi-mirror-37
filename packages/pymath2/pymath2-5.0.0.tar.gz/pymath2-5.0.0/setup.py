#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='pymath2',
    version='5.0.0',
    description='Easy calculations on the command line with Python',
    author='Caleb Bassi',
    url='https://github.com/cjbassi/pymath',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    license='MIT',
    scripts=['scripts/pymath'],
)

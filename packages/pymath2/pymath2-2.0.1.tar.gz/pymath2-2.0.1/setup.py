#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='pymath2',
    version='2.0.1',
    description='Easy calculations on the command line with Python',
    author='Caleb Bassi',
    url='https://github.com/cjbassi/pymath',
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    include_package_data=True,
    license='MIT',
    scripts=['scripts/pymath'],
)

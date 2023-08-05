#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

version = '0.1.2'

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'attachi',
    version = version,
    description = 'Small attachment helper script for openBIS registration.',
    long_description = readme,
    keywords = ['openbis', 'attachment'],
    author = 'Andreas Friedrich',
    author_email = 'andreas.friedrich@uni-tuebingen.de',
    license = license,
    scripts = ['scripts/attachi'],
    install_requires = required,
    packages = find_packages(exclude=('docs')),
    setup_requires=[
        'twine>=1.11.0',
        'setuptools>=38.6.',
    ] + ([] if sys.version_info.minor == 4 else ['wheel>=0.31.0']),
    include_package_data = True
)

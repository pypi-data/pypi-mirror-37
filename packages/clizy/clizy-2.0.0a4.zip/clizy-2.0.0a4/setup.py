#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 6):
    raise RuntimeError("Python < 3.6 is not supported!")

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='clizy',
    version='2.0.0-alpha4',
    description="Command-line interface creation for lazy people using type hints.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/prokopst/clizy',
    packages=find_packages(exclude=['tests']),
    author="Stan Prokop",
    license='Apache 2 License',
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
    ]
)

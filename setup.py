#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = '0.1.0'

setup(
    name='nanonisTCP',
    version=version,
    author='Julian Ceddia',
    author_email='jdceddia@gmail.com',
    description='python module for communicating via nanonis TCP protocal',
    long_description=long_description,
    url='https://github.com/New-Horizons-SPM/nanonisTCP',
    project_urls = {
        "Bug Tracker": "https://github.com/New-Horizons-SPM/nanonisTCP/issues"
    },
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy'],
)

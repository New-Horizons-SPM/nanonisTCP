#!/usr/bin/env python

from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = '1.1.2'

setup(
    name='nanonisTCP',
    version=version,
    author='Julian Ceddia',
    author_email='jdceddia@gmail.com',
    description='python module for communicating via nanonis TCP protocal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/New-Horizons-SPM/nanonisTCP',
    project_urls = {
        "Bug Tracker": "https://github.com/New-Horizons-SPM/nanonisTCP/issues"
    },
    license='MIT',
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
)

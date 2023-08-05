#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup.py: script to facilitate installation of the package
# Author: Ravi Joshi
# Date: 2018/10/02

# import modules
from setuptools import setup, find_packages

# description can be read from README file
with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='whillpy',
    version='0.2',
    author='Ravi Prakash Joshi',
    author_email='joshi.ravi-prakash869@mail.kyutech.jp',
    description='Unofficial python package for WHILL Model CK control',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/ShibataLab/whillpy',
    packages=find_packages(),
    license='MIT',
    install_requires=['pyserial'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

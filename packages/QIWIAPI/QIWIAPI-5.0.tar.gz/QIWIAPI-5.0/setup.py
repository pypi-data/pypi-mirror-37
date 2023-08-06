#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Code by StoNeR 1778
# Soft (c) 2018

from setuptools import setup, find_packages 
from QIWIAPI.__version__ import __version__
 
 
requirements = ['uuid==1.30,<2', 'urllib3==1.23,<2', 'requests==2.19.1,<3', 'idna==2.7,<3', 'chardet==3.0.4,<4', 'certifi==2018.4.16',]
setup_requirements = ['uuid==1.30,<2', 'urllib3==1.23,<2', 'requests==2.19.1,<3', 'idna==2.7,<3', 'chardet==3.0.4,<4', 'certifi==2018.4.16']

setup(
    name='QIWIAPI',
    author='StoNeR 1776',
    author_email='stoner1776@gmail.com',
    description='Anonymous transactions in QIWI wallets',
    license='MIT',
    long_description='See https://github.com/stoner1776/QIWIAPI/',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(include=['QIWIAPI']),
    setup_requires=setup_requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    version=__version__,
    url='https://github.com/stoner1776/QIWIAPI/',
)

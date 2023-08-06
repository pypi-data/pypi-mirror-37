#############################################
# File Name: setup.py
# Author: WEN
# Created Time:  2018-10-20 00:16:21
#############################################

from setuptools import setup ,find_packages

setup(
    name        = 'calculate_expression',
    version     = '1.0.2',
    # py_modules  = ["calculate_expression"],
    author      = 'WEN',
    author_email    = '764499983@qq.com',
    url     = 'https://github.com/GoodManWEN/calculate_expression',
    description = 'simple tool to calculate expressions',
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

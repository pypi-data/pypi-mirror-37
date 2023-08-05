#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: handa
# Mail: 794363716@qq.com
# Created Time:  2018-09-28 14:14:30
#############################################


from setuptools import setup, find_packages

setup(
    name = "reference",
    version="0.0.3",
    keywords = ("pip", "reference", "podspec"),
    description = "Correct the reference",
    long_description = "Correct the reference",
    license = "MIT Licence",

    url="https://github.com/piaoying/reference",
    author="handa",
    author_email="794363716@qq.com",
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # include any *.msg files found in the 'test' package, too:
        'test': ['*.msg'],
    },
    packages = find_packages(),
    include_package_data = True,
    platforms = "macOS",
    install_requires=["tree"],
    entry_points={'console_scripts': [
        "reference = reference.reference:main",
    ]}
)
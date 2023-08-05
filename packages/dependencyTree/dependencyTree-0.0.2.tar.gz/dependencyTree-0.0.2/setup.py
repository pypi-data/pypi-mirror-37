#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "dependencyTree",
    version="0.0.2",
    keywords = ("pip", "dependency", "tree", "podspec"),
    description = "Analyze dependencies between components",
    long_description = "Analyze dependencies between components",
    license = "MIT Licence",

    url="https://github.com/piaoying/dependencyTree",
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
    platforms = "any",
    install_requires=[ "PyYAML"],
    entry_points={'console_scripts': [
        "dependencyTree = dependencyTree.dependencyTree:main",
    ]}
)
# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "shimbase"
VERSION = "1.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ['sphinx>=1.8.1']

setup(
    name=NAME,
    version=VERSION,
    description="Object database layer",
    author_email="monkeeferret@gmail.com",
    url="https://github.com/HogRoast/shimbase/",
    keywords=["Object database layer"],
    license="MIT",
    install_requires=REQUIRES,
    python_requires=">=3.7",
    packages=find_packages(),
    package_data={
        # If any package contains txt, sql, db or tmpl files, include them:
        '': ['*.txt', '*.sql', '*.db', '*.tmpl'],
    },
    include_package_data=True,
    entry_points={},
    long_description="An object oriented database abstraction library. The aim is to provide a simple library for manipulating relational database tables via python objects. The abstraction will allow for any relational database implementation to be plugged in, meaning application code can be written in a database independent fashion."
)


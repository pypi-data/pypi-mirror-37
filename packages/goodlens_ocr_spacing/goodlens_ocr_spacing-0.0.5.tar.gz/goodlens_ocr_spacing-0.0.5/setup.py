# coding: utf-8

"""
    goodlens_ocr_spacing

    Utility package for goodlens product-db

"""


import sys
from setuptools import setup, find_packages
from os import path

NAME = "goodlens_ocr_spacing"
VERSION = "0.0.5"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptoolss

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="",
    author_email="swcbok@gmail.com",
    url="",
    keywords=["GoodLens", "goodlens_ocr_spacing"],
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    """
)

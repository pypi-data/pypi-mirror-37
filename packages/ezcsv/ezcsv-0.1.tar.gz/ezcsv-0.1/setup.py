#!/usr/bin/env python

import setuptools
from distutils.core import setup
import os

# Get the long description from the README file
with open(os.path.join(".", "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ezcsv",
    version="0.1",
    description="Functions to do obvious things with CSVs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Brandon Istenes",
    author_email="brandonesbox@gmail.com",
    url="https://github.com/brandones/ezcsv",
    packages=["ezcsv"],
    project_urls={"Source": "https://github.com/brandones/ezcsv"},
)

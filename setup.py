#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name="std2",
    version="0.1.0",
    description="STD #2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/ms-jpq/std2",
    packages=find_packages(exclude=("tests*",)),
)

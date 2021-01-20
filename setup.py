#!/usr/bin/env python3

from pathlib import Path

from setuptools import find_packages, setup

from std2 import __version__

packages = find_packages(exclude=("tests*",))
package_data = {pkg: ("py.typed",) for pkg in packages}

setup(
    name="std2",
    python_requires=">=3.8.0",
    version=__version__,
    description="STD #2",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="ms-jpq",
    author_email="github@bigly.dog",
    url="https://github.com/ms-jpq/std2",
    packages=packages,
    package_data=package_data,
)

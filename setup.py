# -*- coding: utf-8 -*-
"""Install library with `python setup.py install` or `python setup.py develop`."""

import io
import os

from setuptools import find_packages, setup

DEPENDENCIES = ["Click", "python-decouple", "loguru"]
EXCLUDE_FROM_PACKAGES = []
CURDIR = os.path.abspath(os.path.dirname(__file__))
VERSION = "0.1.0"

with io.open(os.path.join(CURDIR, "README.md"), "r", encoding="utf-8") as f:
    README = f.read()


setup(
    name="ghpm",
    version=VERSION,
    author="Constantino Schillebeeckx",
    include_package_data=True,
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    install_requires=DEPENDENCIES,
    include_package_data=True,
    keywords=[],
    scripts=[],
    entry_points={"console_scripts": ["ghpm=ghpm.main:cli"]},
    # entry_points={"console_scripts": ["pycowsay=pycowsay.main:main"]},
    zip_safe=False,
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python",
    ],
)

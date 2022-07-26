# -*- coding: utf-8 -*-
"""Install library with `python setup.py install` or `python setup.py develop`."""
from setuptools import find_packages, setup

setup(
    name="ghpm",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click", "python-decouple", "loguru"],
    entry_points={
        "console_scripts": [
            "ghpm = ghpm.main:cli",
        ],
    },
)

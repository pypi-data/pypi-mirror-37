#!/usr/bin/env python
import os
from setuptools import find_packages, setup

project = "snark"
version = "0.3.0.1"

#TODO: add description

setup(
    name=project,
    version=version,
    description="Snark AI command line client",
    author="Snark AI Inc.",
    author_email="support@snarkai.com",
    url="https://github.com/snarkai/snark-cli",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords="snark",
    python_requires='>=3',
    install_requires=[
        "click>=6.7,<7",
        "clint>=0.5.1,<1",
        "requests>=2.12.4,<3",
        "requests-toolbelt>=0.7.1,<1",
        "marshmallow>=2.11.1,<3.0.0b0",
        "pytz>=2016.10",
        "tabulate>=0.7.7,<1",
        "outdated"
    ],
    setup_requires=[],
    dependency_links=[],
    entry_points={
        "console_scripts": [
            "snark = snark.main:cli",
            "snark-local = snark.development.local:cli",
        ],
    },
    tests_require=[
        "pytest",
        "mock>=1.0.1",
    ],
)

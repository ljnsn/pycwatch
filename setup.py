#!/usr/bin/env python
"""
Release notes:
* Bump version in pycwatch/__init__.py
* Bump version in CHANGELOG.md
* Update docs where necessary
* Tag version: git tag -a $version -m "version $version"
* Commit and push changes
"""
from pathlib import Path
from setuptools import find_packages, setup


__version__ = None

init_file = Path(__file__).parent / "pycwatch" / "__init__.py"
with init_file.open(encoding="utf-8") as f:
    for line in f:
        if not line.startswith("__version__"):
            continue
        __version__ = line.split("=")[1].strip(" \"'\n")
        break

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    dependencies = [d.strip() for d in f.readlines() if not d.startswith("#")]


setup(
    name="pycwatch",
    version=__version__,
    packages=find_packages(),
    url="https://github.com/iuvbio/pycwatch",
    license="MIT License",
    author="Crypto God",
    author_email="cryptodemigod@protonmail.com",
    description="Implements the Cryptowatch Rest API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=dependencies,
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "requests-mock",
        ]
    },
)

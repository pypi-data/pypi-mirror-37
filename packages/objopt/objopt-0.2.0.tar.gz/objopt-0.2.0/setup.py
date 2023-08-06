#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import os
import sys
import io
from setuptools import find_packages, setup, Command, setup

import objopt

# Package meta-data.
NAME = "objopt"
DESCRIPTION = "Object oriented optimization"
URL = "https://github.com/stsievert/objopt"
EMAIL = "dev@stsievert.com"
AUTHOR = "Scott Sievert"

# What packages are required for this module to be executed?
REQUIRED = ["numpy"]


version = objopt.__version__


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    sys.exit()

if sys.argv[-1] == "tag":
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

with io.open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

requirements = ["numpy"]

if sys.argv[-1] == "readme":
    print(readme)
    sys.exit()


setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=readme,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=["objopt"],
    package_dir={"objopt": "objopt"},
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
    ],
    keywords=["optimization", "machine learning", "theory", "object oriented"],
)

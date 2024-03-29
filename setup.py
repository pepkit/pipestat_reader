#! /usr/bin/env python

import os
import sys

from setuptools import setup

PACKAGE = "pipestat_reader"

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        # DEPENDENCIES.append(line.split("=")[0].rstrip("<>"))
        DEPENDENCIES.append(line)

# 2to3
# if sys.version_info >= (3,):
#     extra["use_2to3"] = True
# extra["install_requires"] = DEPENDENCIES


# Additional files to include with package
def get_static(name, condition=None):
    static = [
        os.path.join(name, f)
        for f in os.listdir(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), name)
        )
    ]
    if condition is None:
        return static
    else:
        return [i for i in filter(lambda x: eval(condition), static)]


# scripts to be added to the $PATH
# scripts = get_static("scripts", condition="'.' in x")
# scripts removed (TO remove this)
scripts = None

with open(PACKAGE + "/_version.py", "r") as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
try:
    import pypandoc

    long_description = pypandoc.convert_file("README.md", "rst")
except (IOError, ImportError, OSError):
    long_description = open("README.md").read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=version,
    description="A generator of pipestat-based APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    keywords="project, metadata, bioinformatics, sequencing, ngs, workflow",
    url="https://github.com/pepkit/" + PACKAGE,
    author="Michal Stolarczyk",
    license="BSD2",
    scripts=scripts,
    include_package_data=True,
    test_suite="tests",
    tests_require=(["mock", "pytest"]),
    setup_requires=(
        ["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []
    ),
    **extra
)

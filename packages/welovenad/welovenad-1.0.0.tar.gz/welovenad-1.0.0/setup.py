#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" This script provides setup requirements to install hrvanalysis via pip"""

import setuptools
from codecs import open
from os import path
import welovenad

# Get long description in READ.md file
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

# get the dependencies in requirements file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements_list = f.read().split('\n')

setuptools.setup(
    name="welovenad",

    # la version du code
    version=welovenad.__version__,

    author="Robin Champseix",
    license="MIT",
    author_email="robin.champseix@gmail.com",
    description="a demo package for NAD !",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://link/of/your/package",

    # include MANIFEST.in
    include_package_data=True,

    # Liste les packages à insérer dans la distribution
    # find_packages() de setuptools qui va cherche tous les packages
    # python recursivement dans le dossier courant.
    packages=setuptools.find_packages(),
    python_requires='>=3.6',

    # Add your project dependencies !
    install_requires=[
        requirements_list
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ]
)

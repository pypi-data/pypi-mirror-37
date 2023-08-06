#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011, Toru Maesaka
# Copyright (c) 2018, Carlos Rodrigues
#
# Redistribution and use of this source code is licensed under
# the BSD license. See COPYING file for license description.


import os

from setuptools import setup


manifest = {
    "name": "python-kyototycoon-ng",
    "version": "0.7.5",
    "description": "Python client for Kyoto Tycoon key-value store",
    "author": "Toru Maesaka",
    "author_email": "dev@torum.net",
    "maintainer": "Carlos Rodrigues",
    "maintainer_email": "cefrodrigues@gmail.com",
    "url": "https://github.com/carlosefr/python-kyototycoon-ng",
    "packages": ["kyototycoon"],
    "license": "BSD",
    "keywords": "Kyoto Tycoon, Kyoto Cabinet",
    "long_description": open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
    ],
    "zip_safe": False,
}

setup(**manifest)


# vim: set expandtab ts=4 sw=4:

#!/usr/bin/env python

from setuptools import setup
import etlite

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='etlite',
    version=etlite.VERSION,
    description='Extract/Transform Light - a simple library for reading delimited files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Sergiy Kuzmenko',
    url='https://github.com/shelldweller/etlite',
    packages=['etlite'],
    license="Public Domain",
    platforms=['any'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Interpreters"
    ],
)

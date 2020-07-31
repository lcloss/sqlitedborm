#!/usr/bin/env python3
#coding: utf-8
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlitedborm",
    version="0.0.1",
    author="Luciano Closs",
    author_email="luciano_closs@hotmail.com",
    description="A SQLite3 database ORM Scheme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lcloss/sl3db.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
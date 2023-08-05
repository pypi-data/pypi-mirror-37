#!/usr/bin/env python
# Thu Oct 18 12:03:02 CST 2018

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmdcall",
    version="0.0.1",
    author="Di Xu",
    author_email="xudifsd@gmail.com",
    description="Utility for quick test python script",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xudifsd/cmdcall",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=["cmdcall"]
)

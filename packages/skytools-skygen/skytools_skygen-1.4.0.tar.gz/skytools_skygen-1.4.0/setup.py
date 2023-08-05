# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="skytools_skygen",
    version="1.4.0",
    author="SkyGen",
    author_email="skygen@alwaysdata.net",
    description="Easily create softwares in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SkyGenProg/SkyTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

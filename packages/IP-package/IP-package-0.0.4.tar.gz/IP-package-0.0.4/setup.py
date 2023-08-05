# -*- coding: UTF-8 -*-
import setuptools
import sys
sys.path.append(r'../../')
with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="IP-package",
    version="0.0.4",
    author="Chao",
    author_email="chao.wang@oyohotels.cn",
    description="A small IP package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=['ippackage'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# -*- coding: UTF-8 -*-
import setuptools
import sys

sys.path.append(r'../../')
with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zymtest2",
    version="0.0.6",
    author="Chao",
    author_email="chao.wang@oyohotels.cn",
    description="A small IP package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
)

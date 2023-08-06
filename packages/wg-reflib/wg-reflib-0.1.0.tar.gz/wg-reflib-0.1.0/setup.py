#! /usr/bin/env python3

import os
from setuptools import setup, find_packages

setup(
    name="wg-reflib",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["doi2bib", "pybtex"],
    extras_require={"dev": ["black", "pre-commit"]},
    version="0.1.0",
    description="Add references to the Wright group library",
    url="http://wright.chem.wisc.edu",
    author="Kyle Sunden",
    license="MIT",
    entry_points={
        "console_scripts": ["wg-reflib=reflib.__init__:main"],
        "gui_scripts": ["wg-reflib-gui=reflib.__init__:gui"],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)

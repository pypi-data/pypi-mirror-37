# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 0):
    sys.exit('Sorry, Python < 3.0 is not supported')

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('rensha256/rensha256.py').read(),
    re.M
).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name="rensha256",
    python_requires='>=3.7',
    packages=find_packages(),
    entry_points={
        "console_scripts": ['rensha256 = rensha256.rensha256:main']
    },
    install_requires=[
        "pathlib"
    ],
    setup_requires=[
        "pathlib"
    ],
    version=version,
    description="Python command line application bare bones template.",
    long_description=long_descr,
    author="Taylor Monacelli",
    author_email="taylormonacelli@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/taylormonacelli/rensha256/issues",
        "Documentation": "https://github.com/taylormonacelli/rensha256",
        "Source Code": "https://github.com/taylormonacelli/rensha256",
    }
)

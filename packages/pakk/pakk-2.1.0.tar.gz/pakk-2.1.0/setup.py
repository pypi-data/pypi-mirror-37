"""
Setup module that generates a distributable package of the pakk library and cli tools.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as readme:
    LONG_DESC = readme.read()

setup(
    name="pakk",
    version="2.1.0",
    author="Tristen Horton",
    author_email="tristen@tristenhorton.com",
    description="A package for encrypting and packing files into a single uncompressed file.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    url="https://github.com/pakk/pakk",
    packages=find_packages(),
    scripts=["bin/pakk"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ]
)

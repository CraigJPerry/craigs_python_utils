#!/usr/bin/env python
# encoding: utf-8


"""My collection of reusable python utilities."""


from setuptools import setup, find_packages


__version__ = "0.1.4"
README = open("README.rst").read()
REQUIREMENTS = open("requirements.txt").readlines()


setup(
    name="craigs_python_utils",
    version=__version__,
    description=__doc__,
    long_description=README,
    author="Craig J Perry",
    author_email="craigp84@gmail.com",
    install_requires=REQUIREMENTS,
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests"]),
    test_suite='nose.collector'
)


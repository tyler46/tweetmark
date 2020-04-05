#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="tweets",
    version="0.0.1",
    description="Receive tweets and store them",
    packages=find_packages(exclude=["test", "test.*"]),
    install_requires=["nameko==2.12.0", "tweepy==3.8.0", "arrow==0.15.5"],
    extras_require={"dev": ["pytest==5.4.1", "coverage==5.0.4", "flake8==3.7.9"]},
    zip_safe=True,
)

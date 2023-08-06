#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as f:
        long_description = f.read()

setup(
    name='blinkcomputing',
    url='https://github.com/blinkcomputing/blink-client',
    version='0.0.5',
    description='Client for Blink Computing service',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License, Version 2.0',
    packages=['blinkcomputing'],
    install_requires=['requests'],
    maintainer="Blink Computing",
    maintainer_email="info@blinkcomputing.co")

#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='events2jsonl',
    version='0.1.0',
    description='Output Windows Events in JSONL format',
    author='devgc',
    url='https://github.com/devgc',
    scripts = [
        'events2jsonl.py'
    ],
    dependency_links = [
    ],
    install_requires = [
    ]
)
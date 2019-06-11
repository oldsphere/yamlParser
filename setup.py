#!/usr/bin/env python
import os
import sys

from setuptools import setup

version = '0.9'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

install_reqs = [
    "ruamel.yaml"
]


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
    except IOError:
        return ""

setup(
    name = "yamlParser",
    version = version,
    author = "Carlos Rubio Abujas",
    author_email = "oldsphere@gmail.com",
    description = ("A customized yaml parser with deep search/replace functions"),
    license = "MIT",
    keywords = "yaml configuration parser",
    url = "",
    packages=['yamlParser'],
    #long_description=read('readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    install_requires=install_reqs
)

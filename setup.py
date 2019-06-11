#!/usr/bin/env python
import os
import sys

from setuptools import setup

with open("./AutoStudies/__version__.py") as version_file:
    version = version_file.read().split("\"")[1]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

install_reqs = [
    "pushbullet.py",
]


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            return f.read()
    except IOError:
        return ""

setup(
    name = "AutoStudies",
    version = version,
    author = "Carlos Rubio",
    author_email = "oldsphere@gmail.com",
    description = ("A Study-Case system to systematic analysis"),
    license = "MIT",
    keywords = "automatization cases simulation studies",
    url = "",
    packages=['AutoStudies'],
    #long_description=read('readme.md'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    install_requires=install_reqs,
    dependency_links=['git+https://github.com/rbrcsk/pushbullet.py/#egg=pushbullet.py']
)

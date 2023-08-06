# -*- coding: utf-8 -*-
import os
import re

from setuptools import find_packages, setup


def read_file(filename):
    """Open and a file, read it and return its contents."""
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path) as f:
        return f.read()


def get_metadata(init_file):
    """Read metadata from a given file and return a dictionary of them"""
    return dict(re.findall("__([a-z]+)__ = '([^']+)'", init_file))


init_path = os.path.join('django_remote_debug', '__init__.py')
init_py = read_file(init_path)
metadata = get_metadata(init_py)


setup(
    name='django-remote-debug',
    version=metadata['version'],
    author=metadata['author'],
    author_email=metadata['email'],
    url=metadata['url'],
    license=metadata['license'],
    description='A Wrapper to Visual Studio remote debugging server for python',
    long_description=read_file('README.rst'),
    packages=find_packages(include=('django_remote_debug*',)),
    install_requires=[
        'ptvsd>=4.0.0',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

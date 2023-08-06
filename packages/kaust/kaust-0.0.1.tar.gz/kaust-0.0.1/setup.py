# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup, find_packages
import sys

VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README.md'))
long_description = f.read().strip()
f.close()

install_requires = [
    'Cython',
    'pymssql',
    'openstacksdk>=0.19.0'
]
tests_require = [
    'nose',
    'coverage',
    'mock',
    'pyaml',
    'nosexcover'
]

setup(
    name = 'kaust',
    description = "Python client for KAUST",
    license="Apache License, Version 2.0",
    url = "https://gitlab.kaust.edu.sa/kaust-rc/kaust-py",
    long_description = long_description,
    version = __versionstr__,
    author = "Antonio Arena",
    author_email = "antonio.arena@kaust.edu.sa",
    packages=find_packages(
        where='.',
        exclude=('tests*', )
    ),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=install_requires,

    test_suite='tests.run_tests.run_all',
    tests_require=tests_require,
)

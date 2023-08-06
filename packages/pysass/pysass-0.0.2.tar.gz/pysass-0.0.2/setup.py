#!/usr/bin/env python
# -*- coding: utf-8 -*-
# read the contents of your README file
from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pysass',
    description='Sass CLI Python: '
    'A wrapper to libsass-python with watchdog capability.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.0.2',
    py_modules=['pysass'],
    packages=[],
    package_data={},
    license='MIT License',
    author='Steeve Chailloux',
    author_email='steevechailloux'
    '@'
    'gmail.com',
    url='https://github.com/WnP/pysass/',
    entry_points={
        'console_scripts': [['pysass = pysass:main'], ],
    },
    install_requires=['libsass', 'watchdog'],
    extras_require={},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
    ],
)

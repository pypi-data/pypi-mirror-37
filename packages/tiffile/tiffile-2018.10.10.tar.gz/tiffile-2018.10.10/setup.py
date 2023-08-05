# -*- coding: utf-8 -*-
# tiffile/setup.py

import sys
import re

from setuptools import setup

buildnumber = ''

with open('tiffile/tifffile.py') as fh:
    code = fh.read()

version = re.search(r"__version__ = '(.*?)'", code).groups()[0]
description = re.search(r'"""(.*)\.\n', code).groups()[0]
readme = re.search(r'[\r\n?|\n]{2}"""(.*)"""[\r\n?|\n]{2}from', code,
                   re.MULTILINE | re.DOTALL).groups()[0]
license = re.search(r'(# Copyright.*?[\r\n?|\n])[\r\n?|\n]+""', code,
                    re.MULTILINE | re.DOTALL).groups()[0]

readme = '\n'.join([description, '=' * len(description)]
                   + readme.splitlines()[1:])
license = license.replace('# ', '').replace('#', '')

if 'sdist' in sys.argv:
    with open('LICENSE', 'w') as fh:
        fh.write(license)
    with open('README.rst', 'w') as fh:
        fh.write(readme)

setup(
    name='tiffile',
    version=version + buildnumber,
    description=description,
    long_description=readme,
    author='Christoph Gohlke',
    author_email='cgohlke@uci.edu',
    url='https://www.lfd.uci.edu/~gohlke/',
    license='BSD',
    packages=['tiffile'],
    py_modules=['tifffile'],
    python_requires='>=2.7',
    install_requires=[
        'numpy>=1.14',
        'imagecodecs>=2018.9.22',
        'pathlib;python_version=="2.7"',
        'enum34;python_version=="2.7"',
        'futures;python_version=="2.7"',
        ],
    extras_require={
        'imshow': ['matplotlib>=2.2'],
        'all': ['matplotlib>=2.2'],
    },
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tifffile = tiffile:main',
            'lsm2bin = tiffile.lsm2bin:main'
            ]},
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
)

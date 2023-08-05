#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = [
        'PyYAML==3.11',
        'requests==2.5.3',
        'ndg-httpsclient==0.5.1;python_version<"2.7.9"',
        'pyOpenSSL==18.0.0;python_version<"2.7.9"',
        'pyasn1==0.4.4;python_version<"2.7.9"'
    ]

about = {}
with open(os.path.join(here, 'gdpy', 'version.py'), 'r'.encode('utf-8')) as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    # long_description=readme,
    packages=['gdpy'],
    install_requires=requires,
    include_package_data=True,
    url=about['__url__'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)

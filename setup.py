#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

setup(
    name='dbaas_nfsaas',
    version='0.7.9',
    description='NFSaaS integration for DBaaS',
    long_description=readme,
    author='Mauro Andre Murari',
    author_email='mauro_murari@hotmail.com',
    url='https://github.com/globocom/dbaas-nfsaas',
    packages=[
        'dbaas_nfsaas',
    ],
    package_dir={'dbaas_nfsaas': 'dbaas_nfsaas'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='dbaas_nfsaas',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)

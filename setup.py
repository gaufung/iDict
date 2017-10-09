#!/usr/bin/env python
# coding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

import dict

setup(
    name='iDict',
    keywords=['dictionary', 'bing dict', 'education'],
    packages=['iDict'],
    url='https://github.com/gaufung/iDict',
    license='MIT',
    author='gau fung',
    author_email='gaufung@outlook.com',
    description='Bing dictionary to look up',
    install_requires=[
        'termcolor', 'bs4', 'requests'
    ],
    entry_point={
        'console_script': [
            'd=dict:run'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
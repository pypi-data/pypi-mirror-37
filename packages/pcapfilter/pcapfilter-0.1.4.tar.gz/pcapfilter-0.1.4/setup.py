#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'watchdog',
    'scapy',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Nahuel Defossé",
    author_email='nahuel.defosse+pip@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python package for packet filtering and manipulation using scapy",
    entry_points={
        'console_scripts': [
            'pcapfilter=pcapfilter.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pcapfilter',
    name='pcapfilter',
    packages=find_packages(include=['pcapfilter']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/D3f0/pcapfilter',
    version='0.1.4',
    zip_safe=False,
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Marcos Alfredo Núñez",
    author_email='mnunez@fleni.org.ar',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="A simple BTS MDX file parser based on BeautifulSoup",
    entry_points={
        'console_scripts': [
            'simplemdx=simplemdx.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU GPLv3 Licence",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='simplemdx',
    name='simplemdx',
    packages=find_packages(include=['simplemdx']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/marnunez/simplemdx',
    version='0.1.9',
    zip_safe=False,
)

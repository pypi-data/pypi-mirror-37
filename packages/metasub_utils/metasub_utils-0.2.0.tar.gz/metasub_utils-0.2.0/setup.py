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
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(dcdanko): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='metasub_utils',
    version='0.2.0',
    description="Utilities for the MetaSUB Consortium",
    long_description=readme + '\n\n' + history,
    author="David C. Danko",
    author_email='dcdanko@gmail.com',
    url='https://github.com/dcdanko/metasub_utils',
    packages=find_packages(include=['metasub_utils']),
    entry_points={
        'console_scripts': [
            'metasub=metasub_utils.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='metasub_utils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

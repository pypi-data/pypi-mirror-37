#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

setup_requirements = [
    # TODO(heathercreech): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'requests'
    # TODO: put package test requirements here
]

setup(
    name='dappy',
    version='2.0.0',
    description="packge to allow defining an API via dictionaries",
    long_description=readme + '\n\n' + history,
    author="Heather Creech",
    author_email='heatherannecreech@gmail.com',
    url='https://gitlab.com/heathercreech/dappy',
    packages=find_packages(include=['dappy']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='dappy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

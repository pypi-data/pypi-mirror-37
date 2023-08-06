#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""


try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.download import PipSession


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

parsed_requirements = parse_requirements(
    'requirements/prod.txt',
    session=PipSession()
)

parsed_test_requirements = parse_requirements(
    'requirements/test.txt',
    session=PipSession()
)

requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]

setup(
    name='nider',
    version='0.5.0',
    description="Python package to add text to images, textures and different backgrounds",
    long_description=readme + '\n\n' + history,
    author="Vladyslav Ovchynnykov",
    author_email='ovd4mail@gmail.com',
    url='https://github.com/pythad/nider',
    packages=find_packages(include=['nider*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='nider',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    test_suite='tests',
    tests_require=test_requirements,
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests>=2.19.1,<3.0.0',
    'uritemplate==3.0.0',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'coverage', 'responses', 'pytest-responses']

setup(
    author="John Storey",
    author_email='hello@storey.io',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Client library for the ICANN Registry Reporting Interface",
    keywords='rri icann registry api',
    python_requires='>=3.6.0',
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    name='rri',
    packages=find_packages(include=['rri']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/storeyio/rri',
    version='0.1.2',
    zip_safe=False,
)

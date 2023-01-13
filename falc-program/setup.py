#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='falc',
    py_modules=['falc'],
    packages=find_packages(),
    version='0.1.0',
    description='Firmware Update Abstraction Layer Command-Line Tool',
    license='Apache 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    url='https://github.com/intel-sandbox/PFU',
    keywords="firmware update",
    python_requires=">=3.10",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.2', 'pytest-cov==3.0.0', 'mock==4.0.3', 'types-mock==4.0.15'],
    test_suite='tests',
)

#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='fall',
    py_modules=['fall'],
    packages=find_packages(),
    package_data={"": ["py.typed"]},
    # include_package_data=True,
    version='0.1.0',
    description='Firmware Update Abstraction Layer',
    license='Apache 2.0',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    url='https://github.com/intel-sandbox/PFU',
    keywords="firmware update",
    python_requires=">=3.10",
    install_requires=['psutil==5.9.1', 'xmlschema==2.0.2', 'defusedxml==0.7.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.1.2', 'pytest-cov==3.0.0', 'mock==4.0.3', 'types-mock==4.0.15'],
    test_suite='tests'
)

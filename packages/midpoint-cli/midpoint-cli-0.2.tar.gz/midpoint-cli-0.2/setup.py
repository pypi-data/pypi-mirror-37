#!/usr/bin/env python3
from setuptools import setup

from midpoint_cli import __version__

setup(
    name='midpoint-cli',
    version=__version__,
    packages=['midpoint_cli'],
    package_dir={'midpoint_cli': 'midpoint_cli'},
    scripts=['midpoint_cli/midpoint-cli'],
    test_suite='test',
    setup_requires=['pytest-runner'],
    install_requires=['clint', 'requests'],
    tests_require=['pytest'],
    url='https://gitlab.com/alcibiade/midpoint-cli',
    license='MIT',
    author='Yannick Kirschhoffer',
    author_email='alcibiade@alcibiade.org',
    description='A command line client to Midpoint Identity Management system.',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)

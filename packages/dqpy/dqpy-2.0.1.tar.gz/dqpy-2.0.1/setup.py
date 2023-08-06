#!/usr/bin/env python

from setuptools import find_packages, setup

__version__ = '2.0.1'

requires = [
    'arrow==0.12.1',
    'emails==0.5.15',
    'PyMySQL==0.9.2',
    'redis==2.10.6',
    'schematics==2.1.0',
    'SQLAlchemy-Utils==0.33.6',
    'SQLAlchemy==1.2.12',
    'toml==0.10.0',
]

setup(
    name='dqpy',
    version=__version__,
    description='Danqing\'s shared Python library',
    author='Danqing Liu',
    author_email='code@danqing.io',
    url='https://github.com/danqing/dqpy',
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts': ['dbadmin=dq.dbadmin:main'],
    },
    zip_safe=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ),
)

# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 0):
    sys.exit('Sorry, Python < 3.0 is not supported')

with open('README.md', 'r') as fp:
    long_description = fp.read()

setup(
    name='py-mocp',
    description='Music On Console python client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.1-rc3',
    author='Dmitriy Poltavchenko',
    author_email='poltavchenko.dmitriy@gmail.com',
    url='https://gitlab.com/zen-tools/py-mocp',
    license='GPL',
    packages=find_packages(exclude=['mocp.bin']),
    include_package_data=True,
    scripts=['mocp/bin/mocp-notify.py'],
    install_requires=[
        'notify2>=0.3',
        'dbus-python>=1.2.4',
    ],
    classifiers=[
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)

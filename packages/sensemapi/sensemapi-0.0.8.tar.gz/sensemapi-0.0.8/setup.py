#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# System modules
import os
import sys
import runpy
from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, errors = 'ignore') as f:
        return f.read()

package = find_packages(exclude=['tests'])[0]

rpm_package = "python3-" + package
try:
    rpm = "rpm" in sys.argv[1]
except IndexError:
    rpm = False

# run setup
setup(
    name=rpm_package if rpm else package,
    description="Pythonic access to the OpenSenseMap API",
    author="Yann Büchau",
    author_email="nobodyinperson@gmx.de",
    keywords="opensensemap,sensemap,api",
    license="GPLv3",
    version=runpy.run_path(os.path.join(package,"version.py"))\
        .get("__version__","0.0.0"),
    url='https://gitlab.com/tue-umphy/python3-sensemapi',
    long_description=read_file("README.md"),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    install_requires=['requests'],
    tests_require=['numpy','pandas'],
    extras_require = {
        'pandas': ['pandas'],
        },
    test_suite='tests',
    packages=[package],
)

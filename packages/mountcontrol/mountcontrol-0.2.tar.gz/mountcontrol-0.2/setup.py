############################################################
# -*- coding: utf-8 -*-
#
# MOUNTCONTROL
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
import platform
from setuptools import setup
# external packages
# local imports
import mountcontrol.mount

setup(
    name='mountcontrol',
    version=0.2,
    packages=[
        'mountcontrol',
        'mountcontrol.test',
    ],
    python_requires='~=3.6.5',
    install_requires=[
        'PyQt5==5.11.2',
        'numpy==1.15.2',
        'skyfield==1.9',
    ],
    url='https://github.com/mworion/mountcontrol',
    license='APL 2.0',
    author='mw',
    author_email='michael@wuertenberger.org',
    description='tooling for a 10micron mount',
)


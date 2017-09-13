"""
    USAGE IN TERMINAL .. :
        $ python3 setup.py py2app
    *** validation test on env: Python v3.5, py2app v0.13
"""
import os
from setuptools import setup

APP = ['Converter.py']
NAME = 'Color Converter'
DATA_FILES = [('', ['img']), ]
OPTIONS = {'iconfile': 'img/logo.icns', }
SETUP_REQUIRES = ['py2app']

setup(
    app=APP,
    name=NAME,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=SETUP_REQUIRES,
)

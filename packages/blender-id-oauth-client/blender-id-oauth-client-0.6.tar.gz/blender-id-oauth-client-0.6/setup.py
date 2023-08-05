#!/usr/bin/env python3

import os
import pathlib
from setuptools import find_packages, setup

MY_DIR = pathlib.Path(__file__).absolute().parent
with open(MY_DIR / 'README.rst') as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(MY_DIR)

setup(
    name='blender-id-oauth-client',
    version='0.6',

    packages=find_packages(exclude=('tests.*', 'tests', 'example')),
    python_requires=">=3.6",
    install_requires=[
        'Django>=2.1',
    ],
    zip_safe=True,
    include_package_data=True,

    license='GNU General Public License v2 (GPLv2)',
    description='A Django app to authenticate against Blender ID.',
    long_description=README,
    url='https://gitlab.com/blender-institute/blender-id-oauth-client',
    author='Sybren A. Stüvel',
    author_email='sybren@blender.studio',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)

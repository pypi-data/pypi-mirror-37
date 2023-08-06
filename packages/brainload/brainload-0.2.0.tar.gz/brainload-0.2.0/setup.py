#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='brainload',
    version='0.2.0',
    description='Load FreeSurfer brain imaging data with minimal cognitive load',
    long_description='Provides a high-level interface for loading FreeSurfer brain imaging data by wrapping around nibabel.',
    keywords='neuroimaging freesurfer nibabel load mgh curv',
    author='Tim Schäfer',
    author_email='ts+code@rcmd.org',
    url='https://github.com/dfsp-spirit/brainload',
    packages=find_packages(where='src'),
    classifiers = ['Development Status :: 3 - Alpha',     # See https://pypi.org/pypi?%3Aaction=list_classifiers for full classifier list
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7'],
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    install_requires=['numpy', 'nibabel'],
    package_dir = {'': 'src'},                               # The root directory that contains the source for the modules (relative to setup.py) is ./src/,
    include_package_data=True,                               # respect MANIFEST.in at install time
    zip_safe=False
)

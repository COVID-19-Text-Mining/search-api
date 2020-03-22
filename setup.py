#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='covidscholar-search-api',
    version='0.0.1',
    description='The API powering searches of the CovidScholar database',
    long_description=readme,
    author='CovidScholar Team',
    author_email='amalietrewartha@lbl.gov',
    url='https://github.com/COVID-19-Text-Mining/search-api',
    license=license,
    include_package_data=True,
    packages=find_packages()
)

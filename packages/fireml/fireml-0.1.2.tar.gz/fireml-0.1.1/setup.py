#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='fireml',
      version='0.1.1',
      description='fireml machine learning framework',
      author='Anatoly Belikov',
      author_email='awbelikov@gmail.com',
      url='https://bitbucket.org/noSkill/fireml',
      packages=['fireml', 'scripts',],
      scripts=['bin/fire'],
      install_requires=[
          'Theano',
          'numpy',
          'pillow'],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )

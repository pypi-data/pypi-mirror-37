#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(name='pocoui_lib',
      version='0.0.1',
      description='pocoui lib for souche-inc airtest project',
      url='',
      author='mizhdi',
      author_email='mizhdi@gmail.com',
      license='MIT',
      platforms = "any",
      install_requires = ["pocoui"],
      packages = find_packages(),
      zip_safe=False)

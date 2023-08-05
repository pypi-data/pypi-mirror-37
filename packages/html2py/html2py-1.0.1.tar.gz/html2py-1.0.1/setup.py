#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
import html2py


def readme():
    """Load readme."""
    with open('README.md') as f:
        return f.read()


setup(name='html2py',
      version=html2py.__version__,
      description='html2py is a tool for converting an html file in python language and viceversa.',
      long_description=readme(),
      url='http://gitlab.com/trollodel/html2py',
      keywords='yattag generation html2py code_generator tool',
      author='trollodel',
      license='LGPLv2.1',
      scripts=['html2py.py'],
      packages=['html2py'],
      install_requires=[
          'lxml',
          'yattag',
      ],
      zip_safe=False)

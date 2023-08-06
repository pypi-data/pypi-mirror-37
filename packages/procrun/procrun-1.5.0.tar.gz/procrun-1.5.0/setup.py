#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import procrun
setup(name='procrun',
      version=procrun.__version__,
      description=procrun.__doc__.split('\n')[0],
      long_description=procrun.__doc__,
      py_modules=['procrun'],
      url='https://github.com/val-labs/procrun',
      license='MIT',
      platforms='any',
      install_requires=[])

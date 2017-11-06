#!/usr/bin/env python

"""
Package setup script.

Copyright 2017 Leon Helwerda

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup, find_packages
from expression import __version__

setup(name='expression-parser',
      version=__version__,
      description='Sandboxed expression parser',
      long_description='''Python sandboxed expression parser.
This parser can calculate the results of a single simple expression,
disallowing any complicated functions or control structures, with support for
custom variable and function environment contexts.''',
      author='Leon Helwerda',
      author_email='l.s.helwerda@liacs.leidenuniv.nl',
      url='https://github.com/lhelwerd/expression-parser',
      license='Apache License, Version 2.0',
      packages=find_packages(exclude=['tests*']),
      entry_points={
          'console_scripts': ['expression = expression.interpreter:main']
      },
      include_package_data=True,
      install_requires=[],
      test_suite='tests',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Interpreters'],
      keywords=['expression', 'parser', 'sandbox'])

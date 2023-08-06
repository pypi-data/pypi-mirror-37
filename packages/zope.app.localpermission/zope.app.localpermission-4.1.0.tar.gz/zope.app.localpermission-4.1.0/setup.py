##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.app.localpermission package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

version = '4.1.0'

tests_require = [
    'zope.annotation',
    'zope.configuration',
    'zope.testing',
    'zope.testrunner',
]

setup(name='zope.app.localpermission',
      version=version,
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Local Persistent Permissions for zope.security',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
          ),
      keywords="zope security persistent local permission",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      url='https://github.org/zopefoundation/zope.app.localpermission',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      install_requires=[
          'setuptools',
          'persistent',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.location',
          'zope.security',
      ],
      tests_require=tests_require,
      extras_require={
          'test': tests_require,
      },
      include_package_data=True,
      zip_safe=False,
)

##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.form package
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

tests_require = [
    'zc.sourcefactory',
    'zope.container',
    'zope.principalregistry',
    'zope.site',
    'zope.traversing',
    'zope.app.appsetup',
    'zope.testing',
    'zope.testrunner',
    'zope.app.wsgi >= 4.1.0',
    'webtest',
]

setup(name='zope.app.form',
      version='5.1.0',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='The Original Zope 3 Form Framework',
      long_description=(
          read('README.rst')
          + '\n\n' +
          'Detailed documentation:\n'
          + '\n\n' +
          read('CHANGES.rst')
          ),
      keywords="zope3 form widget zcml",
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
      url='https://github.com/zopefoundation/zope.app.form',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      extras_require={
          'test': tests_require
      },
      install_requires=[
          "setuptools",
          "transaction",
          "zope.formlib >= 4.3",
          "zope.browser >= 2.1",
          "zope.browserpage >= 3.10.1",
          "zope.browsermenu",
          "zope.component",
          "zope.configuration >= 4.1.0",
          "zope.datetime",
          "zope.exceptions",
          "zope.i18n",
          "zope.interface",
          "zope.proxy",
          "zope.publisher >= 4.3.1",
          "zope.schema >= 4.4.2",
          "zope.security",
      ],
      include_package_data=True,
      zip_safe=False,
)

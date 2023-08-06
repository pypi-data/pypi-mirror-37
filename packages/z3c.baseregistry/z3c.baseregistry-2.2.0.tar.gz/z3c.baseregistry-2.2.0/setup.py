##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Setup
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()

tests_require = [
    'zope.app.appsetup',
    'zope.app.authentication',
    'zope.app.basicskin >= 4.0.0',
    'zope.app.container >= 4.0.0',
    'zope.app.form >= 5.0.0',
    'zope.app.publisher',
    'zope.app.publication',
    'zope.app.rotterdam >= 4.0.0',
    'zope.app.schema >= 4.0.0',
    'zope.app.wsgi',

    'zope.browserpage',
    'zope.browserresource',
    'zope.container',
    'zope.formlib',
    'zope.login',
    'zope.principalannotation',
    'zope.principalregistry',
    'zope.publisher',
    'zope.securitypolicy',
    'zope.testbrowser >= 5.2',
    'zope.testing',
    'zope.testrunner',
    'zope.traversing >= 4.1.0',

    'webtest',
]

setup(
    name="z3c.baseregistry",
    version='2.2.0',
    author="Stephan Richter, Roger Ineichen and the Zope Community",
    author_email="zope-dev@zope.org",
    description="Manage IComponents instances using Python code and ZCML.",
    long_description=(
        read('README.rst')
        + '\n\n' +
        'Detailed Documentation\n'
        '======================'
        + '\n\n' +
        read('src', 'z3c', 'baseregistry', 'README.rst')
        + '\n\n' +
        read('CHANGES.rst')
        ),
    license="ZPL 2.1",
    keywords="zope3 z3c component global registry baseregistry",
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
        'Framework :: Zope :: 3'
    ],
    url='https://github.com/zopefoundation/z3c.baseregistry',
    packages=find_packages('src'),
    include_package_data=True,
    package_dir={'': 'src'},
    namespace_packages=['z3c'],
    extras_require={
        'test': tests_require,
        'zmi': [
            'zope.formlib',
        ],
    },
    tests_require=tests_require,
    install_requires=[
        'setuptools',
        'zope.component[hook,zcml] >= 4.5.0',
        'zope.configuration >= 4.3.0',
        'zope.i18nmessageid >= 2.2',
        'zope.interface',
        'zope.schema >= 4.9.0',
        'zope.site',
    ],
    zip_safe=False,
)

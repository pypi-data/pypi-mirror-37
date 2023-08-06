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
"""Base Components test setup

"""

__docformat__ = "reStructuredText"
import doctest
import unittest
from zope.testing import renormalizing
from zope.testing.cleanup import CleanUp
from zope.component.testing import tearDown
from zope.testing import module

def setUp(test):
    CleanUp().setUp()
    module.setUp(test, name='README')

def tearDown(test):
    module.tearDown(test, name='README')
    CleanUp().tearDown()

def test_suite():
    return unittest.TestSuite((
            doctest.DocFileSuite(
                '../README.rst',
                setUp=setUp, tearDown=tearDown,
                optionflags=(doctest.NORMALIZE_WHITESPACE
                             | doctest.ELLIPSIS
                             | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2),
                checker=renormalizing.RENormalizing(),
            ),
    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

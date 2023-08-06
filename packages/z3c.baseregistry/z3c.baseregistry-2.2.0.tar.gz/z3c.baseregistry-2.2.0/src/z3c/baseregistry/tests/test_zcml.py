##############################################################################
#
# Copyright (c) 2017 Zope Foundation and Contributors.
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

import unittest

from z3c.baseregistry import zcml

class TestActionsProxy(unittest.TestCase):

    def _makeOne(self, l=None):
        l = l or []
        return l, zcml.ActionsProxy(l, self)

    def test_set_decorates(self):
        l, proxy = self._makeOne(['abc'])
        proxy[0] = {'discriminator': 'foo'}
        self.assertEqual([{'discriminator': (self, 'foo')}], l)

    def test_slice_decorates(self):
        l, proxy = self._makeOne(['abc'])
        proxy[:] = [{'discriminator': 'foo'}]
        self.assertEqual([{'discriminator': (self, 'foo')}], l)

    def test_iadd_decorates(self):
        l, proxy = self._makeOne()
        proxy += [{'discriminator': 'foo'}]
        self.assertEqual([{'discriminator': (self, 'foo')}], l)

    def test_insert_decorates(self):
        l, proxy = self._makeOne(['abc'])
        proxy.insert(0, {'discriminator': 'foo'})
        self.assertEqual([{'discriminator': (self, 'foo')}, 'abc'], l)

    def test_extend_decotares(self):
        l, proxy = self._makeOne(['abc'])
        proxy.extend(({'discriminator': 'foo'},))
        self.assertEqual(['abc', {'discriminator': (self, 'foo')}], l)

    def test_proxy(self):
        l, proxy = self._makeOne()
        self.assertEqual(l.index, proxy.index)

    def test_len(self):
        l, proxy = self._makeOne(['abc'])
        self.assertEqual(len(l), len(proxy))
        self.assertEqual(1, len(proxy))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

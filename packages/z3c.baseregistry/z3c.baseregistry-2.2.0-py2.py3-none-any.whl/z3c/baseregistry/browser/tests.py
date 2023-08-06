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
"""Test setup for Base setting UI tests.

"""

__docformat__ = "reStructuredText"
import doctest
import unittest
import zope.component
import zope.interface

from zope.testing import renormalizing
from zope.app.wsgi.testlayer import BrowserLayer
from zope.testbrowser.wsgi import TestBrowserLayer

from z3c.baseregistry import baseregistry
from z3c.baseregistry import browser as z3c_browser

from zope.interface import implementer
from zope.browsermenu.menu import getFirstMenuItem
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserPublisher


custom = baseregistry.BaseComponents(
    zope.component.globalSiteManager, 'custom')


class IExample(zope.interface.Interface):
    name = zope.interface.Attribute('Name of Example')

@zope.interface.implementer(IExample)
class Example(object):

    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<%s %r>' %(self.__class__.__name__, self.name)

example1 = Example('example1')
example2 = Example('example2')
example3 = Example('example3')
example4 = Example('example4')


def addBasesSelection(browser, bases):
    # Get the form
    from webtest.forms import MultipleSelect
    from zope.testbrowser.browser import ListControl

    form = browser.getForm('zc.page.browser_form')
    webtest_form = form._form # XXX: Private API

    # Create the select tag
    webtest_select = MultipleSelect(webtest_form, None,
                                    name="form.__bases__",
                                    pos=0,
                                    id="form.__bases__")
    # Add the options.
    # Be careful to keep the option indexes in the order that matches
    # the test.
    options = [(x, False, x) for x in bases]
    webtest_select.options.extend(options)
    # Select them.
    webtest_select.select_multiple(texts=bases)

    # Add the select tag to the form
    webtest_form.fields['form.__bases__'] = [webtest_select]
    webtest_form.field_order.append(('form.__bases__', webtest_select))
    # And the browser
    select = ListControl(webtest_select, form, 'select', browser)
    form.controls.append(select)

@implementer(IBrowserPublisher)
class ManagementViewSelector(BrowserView):
    """View that selects the first available management view.

    Support 'zmi_views' actions like: 'javascript:alert("hello")',
    '../view_on_parent.html' or '++rollover++'.
    """
    # Copied from zope.app.publication
    # Simplified to assert just the test case we expect.

    def browserDefault(self, request):
        return self, ()

    def __call__(self):
        item = getFirstMenuItem('zmi_views', self.context, self.request)
        assert item
        redirect_url = item['action']
        if not redirect_url.lower().startswith(('../', 'javascript:', '++')):
            self.request.response.redirect(redirect_url)
            return u''
        raise AssertionError("Should not get here") # pragma: no cover

class LoginLogout(object):
    # Dummy implementation of zope.app.security.browser.auth.LoginLogout

    def __call__(self):
        return None

class _Z3CRegistryLayer(TestBrowserLayer,
                        BrowserLayer):
    pass

Z3CRegistryLayer = _Z3CRegistryLayer(z3c_browser)

def test_suite():

    readme = doctest.DocFileSuite(
        'README.rst',
        globs={
            'IExample': IExample,
            'addBasesSelection': addBasesSelection,
            'getRootFolder': Z3CRegistryLayer.getRootFolder,
        },
        optionflags=(renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2
                     | doctest.ELLIPSIS
                     | doctest.NORMALIZE_WHITESPACE),
        checker=renormalizing.RENormalizing(),
    )
    readme.layer = Z3CRegistryLayer
    suite = unittest.TestSuite((readme,))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

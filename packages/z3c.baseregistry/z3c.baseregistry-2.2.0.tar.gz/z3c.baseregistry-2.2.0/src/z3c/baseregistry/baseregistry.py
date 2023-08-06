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
"""Base Components support

"""
__docformat__ = "reStructuredText"
from zope.component import globalregistry
from zope.interface.interfaces import IComponents

def BC(components, name):
    return components.getUtility(IComponents, name)

class BaseComponents(globalregistry.BaseGlobalComponents):
    """An ``IComponents`` implementation that serves as base for other
    components."""

    def __init__(self, parent, *args, **kw):
        self.__parent__ = parent
        super(BaseComponents, self).__init__(*args, **kw)

    def __reduce__(self):
        # Global site managers are pickled as global objects
        return BC, (self.__parent__, self.__name__)

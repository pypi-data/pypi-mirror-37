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
"""Setting bases for local sites.

"""

__docformat__ = "reStructuredText"
import zope.interface

from zope import component
from zope.component import globalregistry
from zope.interface.interfaces import IComponents

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zope.i18nmessageid import ZopeMessageFactory as _
from zope.formlib import form
from zope.security.proxy import removeSecurityProxy
from zope.site.interfaces import ILocalSiteManager

BASENAME = _('-- Global Base Registry --')
PARENTNAME = _('-- Parent Local Registry --')


@zope.interface.provider(zope.schema.interfaces.IVocabularyFactory)
class BaseComponentsVocabulary(SimpleVocabulary):
    """A vocabulary for ``IComponents`` utilities."""

    def __init__(self, context):
        terms = []
        utils = set()

        # add available registry utilities
        for name, util in component.getUtilitiesFor(IComponents, context):
            terms.append(SimpleTerm(util, name))
            utils.add(util)

        # add location parent registry if any
        lsm = [removeSecurityProxy(sm)
               for sm in context.__bases__
               if sm not in utils and ILocalSiteManager.providedBy(sm)]
        lsm = [SimpleTerm(x, PARENTNAME) for x in lsm[:1]]
        terms.extend(lsm)

        # add the base registry
        terms.append(SimpleTerm(globalregistry.base, BASENAME))

        super(BaseComponentsVocabulary, self).__init__(terms)

class IComponentsBases(zope.interface.Interface):
    """An interface describing the bases API of the IComponents object."""

    __bases__ = zope.schema.List(
        title=_('Bases'),
        description=_('The base components registires of this registry.'),
        value_type=zope.schema.Choice(vocabulary='Base Components'),
        required=True)


class SetBasesPage(form.EditForm):
    """A page to set the bases of a local site manager"""
    form_fields = form.FormFields(IComponentsBases)

# -*- coding: utf-8 -*-

from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel.model import Schema

from zope.i18nmessageid import MessageFactory

from collective.transform.xtags.widgets.widget import XtagsFieldWidget

_ = MessageFactory('collective.transform.xtags')


class IXtagsBehavior(form.Schema):
    """ A Quark Xpress Xtags text field"""

    dexteritytextindexer.searchable('qrktext')


    qrktext = schema.Text(
    	title=u"Quark Xpress Tags text",
    	description=u"Note: Preview is updated when hitting enter. Use utf-8 if mass uploading",
    )

    form.widget(
         qrktext=XtagsFieldWidget,
    )


alsoProvides(IXtagsBehavior, IFormFieldProvider)

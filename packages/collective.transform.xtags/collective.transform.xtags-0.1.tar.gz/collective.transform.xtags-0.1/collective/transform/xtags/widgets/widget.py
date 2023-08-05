# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import zope.component
import zope.interface
import zope.schema.interfaces
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text
from lxml.etree import tostring, fromstring
from collective.transform.xtags.quark_tagged_text import to_xml
#from collective.transform.xtags.interfaces import IXtagsSettings

import logging as log

def get_xtags(tagged_text):
    log.info('getting xtags!')
    try:
        element_tree = to_xml(tagged_text, extra_tags_to_keep={}, css=True)
        serialised_xml = tostring(element_tree, encoding='utf-8')
        return serialised_xml

    except:
        return '<p class="error">[rendering error]<p>'

class IXtagsWidget(interfaces.IWidget):
    """Xtags widget."""


class XtagsWidget(text.TextWidget):
    """Xtags Widget"""
    
    def render_html(self):
        context = self.context
        
        try:
            return context.rendered_html
        except:
            tagged_text = self.value
            context.rendered_html = get_xtags(tagged_text)
            return context.rendered_html
            
    zope.interface.implementsOnly(IXtagsWidget)

def XtagsFieldWidget(field, request):
    """IFieldWidget factory for XtagsWidget."""
    return widget.FieldWidget(field, XtagsWidget(request))
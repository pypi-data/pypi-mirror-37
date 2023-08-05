from plone import api
from zope.i18nmessageid import MessageFactory
from lxml.etree import tostring
from collective.transform.xtags.quark_tagged_text import to_xml
import transaction

from Products.statusmessages.interfaces import IStatusMessage

_ = MessageFactory('collective.transfrom.xtags')
 

def make_html(self, context):
    """generate html from xtags"""
    tagged_text = self.qrktext 
    try:
        element_tree = to_xml(tagged_text, extra_tags_to_keep={}, css=True)
        serialised_xml = tostring(element_tree, encoding='utf-8')
        self.rendered_html = serialised_xml

    except:
        pass
        #self.rendered_html = '<p class="error">[rendering error]<p>'  
        
    self.reindexObject()  
        


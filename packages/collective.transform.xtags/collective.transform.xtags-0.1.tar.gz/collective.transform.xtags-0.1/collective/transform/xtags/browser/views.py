# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from lxml.etree import tostring
from collective.transform.xtags.quark_tagged_text import to_xml

from tempfile import TemporaryFile

#from plone.memoize.view import memoize

def get_xtags(tagged_text):
    try:
        element_tree = to_xml(tagged_text, extra_tags_to_keep={}, css=True)
        serialised_xml = tostring(element_tree, encoding='utf-8')
        return serialised_xml

    except:
        return '<p class="error">[rendering error]<p>'

class RenderFromXtags(BrowserView):
    """ quark xtags to html.    """

    def __call__(self, *args, **kw):
        return self.render_xtags()

    def render_xtags(self):
        """Return quark xtags as a stringified HTML document."""
        tagged_text = self.request.tagged_text
        #remove * in tags
        #pattern = re.compile(r"\<.*?\>")
        #tagged_text = pattern.sub(lambda match: match.group(0).replace('*', "") ,self.request.tagged_text)
        return get_xtags(tagged_text.decode('utf-8'))


class QrkTagsView(BrowserView):
    """ Quark Tags view template"""
    
    def render_html(self):
        context = self.context
        try:
            return context.rendered_html
        except:
            tagged_text = context.qrktext
            context.rendered_html = get_xtags(tagged_text.decode('utf-8'))
            return context.rendered_html   
        
class XTagsExporter(BrowserView):

    def __init__(self, context, request):
        super(XTagsExporter, self).__init__(context, request)

    def __call__(self, REQUEST):
        '''Saves the tags file as a .xtg file,
        '''
        request = self.request
        context = self.context
        file_name = self.context.getId()

        if not file_name.endswith('.xtg'):
            file_name = file_name + '.xtg'

        #xtags = self.context.qrktext.getRaw(obj)
        tags = self.context.qrktext


        # Add header
        dataLen = len(tags)
        R = self.request.RESPONSE
        R.setHeader('Content-Length', dataLen)
        R.setHeader('Content-Type', 'text/xtg')
        R.setHeader('Content-Disposition', 'attachment; filename=%s' % file_name)

        #return thefields
        return tags

from Products.CMFCore.utils import getToolByName

mimetype = 'text/x-xtags'
transform = 'xtags_to_html'

def registerMimetype(portal):
    """Add text/x-tags to the mimetype registry"""
    mime_reg = getToolByName(portal, 'mimetypes_registry')
    if not mime_reg.lookup(mimetype):
        mime_reg.manage_addMimeType(
            id = "XTags to html",
            mimetypes = [mimetype],
            extensions = None,
            icon_path = "text.png"
        )

def uninstallMimetype(portal):
    """Delete the txt2tags mimetype"""
    mime_reg = getToolByName(portal, 'mimetypes_registry')
    if mimetype in mime_reg.objectIds():
        mime_reg.manage_delObjects([mimetype])

def installTransform(portal):
    """Install txt2tags to html transform"""
    transforms = getToolByName(portal, 'portal_transforms')
    if transform not in transforms.objectIds():
        transforms.manage_addTransform(
            transform,
            'collective.transform.xtags.%s' % transform
        )

def uninstallTransform(portal):
    """Uninstall xtags to html transform"""
    transforms = getToolByName(portal, 'portal_transforms')
    transforms.unregisterTransform(transform)

def importVarious(context):
    """Various import step code"""
    marker_file = 'collective-transform-xtags.txt'
    if context.readDataFile(marker_file) is None:
        return
    #portal = context.getSite()
    #registerMimetype(portal)
    #installTransform(portal)
    return


def importVariousUninstall(context):
    """Various uninstall step code"""
    marker_file = 'collective-transform-xtags-uninstall.txt'
    if context.readDataFile(marker_file) is None:
        return
    #portal = context.getSite()
    #uninstallMimetype(portal)
    #uninstallTransform(portal)
    return

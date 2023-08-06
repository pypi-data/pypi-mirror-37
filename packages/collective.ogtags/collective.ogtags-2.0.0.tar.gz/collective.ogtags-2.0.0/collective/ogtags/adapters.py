from zope.interface import implementer

from collective.ogtags.interfaces import IOGTagsImageProvider


@implementer(IOGTagsImageProvider)
class OGTagsImageDexterityProvider(object):

    def __init__(self, context):
        self.context = context

    def getOGTagsImage(self):
        """ Tries to return standard image fields named 'image' and 'lead image'
            Returns None in case of failure"""
        for fieldname in ["image", "leadImage"]:
            try:
                getattr(self.context, fieldname)
                return self.context, fieldname
            except AttributeError:
                pass
        return


@implementer(IOGTagsImageProvider)
class OGTagsImageArchetypeProvider(object):

    def __init__(self, context):
        self.context = context

    def getOGTagsImage(self):
        """ Tries to return standard image fields named 'image' and 'lead image'
            Returns None in case of failure"""
        for fieldname in ["image", "leadImage"]:
            image_field = self.context.getField(fieldname)
            if image_field:
                return self.context, fieldname
        return

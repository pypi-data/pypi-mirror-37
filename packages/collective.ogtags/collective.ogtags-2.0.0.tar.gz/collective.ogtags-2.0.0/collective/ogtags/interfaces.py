from zope.interface import Interface

class IOGTagsImageProvider(Interface):
    """Adapter to get the image that will be used by ogtags viewlet."""

    def getOGTagsImage(self):
        """ Get the context and Image fieldname that will be used by ogtags.
        to generate the scales.

        @return: a tuple in the form: (context, fieldname, ) or None.
        Context is most likely to be (like in the default adapters) the adapted
        context but custom implementations could return parent folders, the
        first Image portal_type contained by the current context or any other
        catalog search result that suits your needs.
        """

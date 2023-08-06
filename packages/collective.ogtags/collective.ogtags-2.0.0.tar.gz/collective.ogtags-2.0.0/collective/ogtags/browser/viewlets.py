from Acquisition import aq_inner

from collective.behavior.seo.interfaces import ISEOFieldsMarker
from collective.ogtags.browser.controlpanel import IOGTagsControlPanel
from collective.ogtags.interfaces import IOGTagsImageProvider
from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import getSiteLogo
from Products.CMFPlone.utils import safe_unicode
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryMultiAdapter


class OGTagsViewlet(ViewletBase):

    def meta_tags(self):
        try:
            self.settings = getUtility(
                IRegistry).forInterface(IOGTagsControlPanel)
        except (ComponentLookupError, KeyError):
            # Note: a KeyError happens when we have added a field to the
            # interface but haven't upgraded yet.
            return
        if not self.settings.enabled:
            return
        context = aq_inner(self.context)
        tags = {}

        # Basic properties
        title = context.title
        description = context.Description()
        url = context.absolute_url()

        # Allow overrides from quintagroup.seoptimizer
        seo = queryMultiAdapter(
            (context, self.request), name='seo_context')
        if seo is not None:
            if seo['has_seo_title']:
                title = safe_unicode(seo["seo_title"])
            if seo['has_seo_description']:
                description = safe_unicode(seo["seo_description"])
            if seo['has_seo_canonical']:
                url = safe_unicode(seo["seo_canonical"])

        # Allow overrides from collective.behavior.seo
        if ISEOFieldsMarker.providedBy(context):
            if context.seo_title:
                title = safe_unicode(context.seo_title)
            if context.seo_description:
                description = safe_unicode(context.seo_description)

        # set title
        if title:
            tags['og:title'] = title
            tags['twitter:title'] = title

        # set description
        if description:
            tags['og:description'] = description
            tags['twitter:description'] = description

        # set url
        if url:
            tags['og:url'] = url

        # social media specific
        if self.settings.fb_id:
            tags['fb:app_id'] = self.settings.fb_id
        if self.settings.fb_username:
            tags['og:article:publisher'] = 'https://www.facebook.com/' \
                + self.settings.fb_username
        if self.settings.tw_id:
            tags['twitter:site'] = self.settings.tw_id
        tags['twitter:card'] = u'summary'

        # misc
        tags['og:type'] = u'website'
        if self.settings.og_site_name:
            tags['og:site_name'] = self.settings.og_site_name
        if self.settings.pinterest_id:
            tags['p:domain_verify'] = self.settings.pinterest_id

        return tags

    def image_tags(self):
        tags = []
        context = aq_inner(self.context)
        try:
            self.settings = getUtility(
                IRegistry).forInterface(IOGTagsControlPanel)
        except (ComponentLookupError, KeyError):
            return
        if not self.settings.enabled:
            return

        default_image = self.default_image(self.settings.default_img)
        try:
            image_provider = IOGTagsImageProvider(context)
        except TypeError:
            return default_image
        result = image_provider.getOGTagsImage()
        if result is None:
            return default_image
        image, fieldname = result
        try:
            scales = image.restrictedTraverse('@@images', None)
        except (AttributeError, KeyError):
            scales = None
        if not image or not fieldname or not scales:
            return default_image
        tag_scales = []
        for scale in [
                'og_fbl',
                'og_fb',
                'og_tw',
                'og_ln']:
            try:
                image = scales.scale(fieldname, scale=scale)
                if not image:
                    continue
            except AttributeError:
                continue
            tag = {}
            if scale == 'og_tw':
                tag['twitter:image'] = image.url
            else:
                if (image.width, image.height) not in tag_scales:
                    tag['og:image'] = image.url
                    tag['og:image:width'] = image.width
                    tag['og:image:height'] = image.height
                    tag_scales.append((image.width, image.height))
            tags.append(tag.copy())
        return tags or default_image

    def default_image(self, image):
        if image is not None:
            portal_state = getMultiAdapter(
                 (self.context, self.request), name=u'plone_portal_state')
            site_root_url = portal_state.navigation_root_url()
            image_url = '%s%s' % (site_root_url, image)
        else:
            image_url = getSiteLogo()

        twitter_tag = {}
        twitter_tag['twitter:image'] = image_url
        og_tag = {}
        og_tag['og:image'] = image_url
        return [twitter_tag, og_tag]

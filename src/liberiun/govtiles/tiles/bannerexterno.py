# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.namedfile.field import NamedBlobImage as NamedImage

from collective.cover import _


class IBannerExternoTile(IPersistentCoverTile):
    """
    """
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    subtitle = schema.Text(
        title=_(u'Subtitle'),
        required=False,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False,
    )

    image = NamedImage(
        title=_(u'Image'),
        required=False,
    )

    url = schema.TextLine(
        title=u'URL',
        required=False,
    )


class BannerExternoTile(PersistentCoverTile):
    is_configurable = True

    def get_image(self):
        conf = self.get_tile_configuration().get('image', {})
        position = conf.get('position', '')
        return {
            'class': position,
        }

    def get_field_image(self):
        for field in self.get_configured_fields():
            if field['id'] == 'image':
                return field

    def thumbnail(self, field, scales):
        scale = field.get('scale', 'large')
        return scales.scale('image', scale)

    def get_dados(self):
        self.get_image()
        return {
            'title': self.data.get('title', ''),
            'title_htmltag': self.get_tile_configuration()['title']['htmltag'],
            'subtitle': self.data.get('subtitle', ''),
            'description': self.data.get('description', ''),
            'url': self.data.get('url', ''),
            'image': self.get_image()
        }

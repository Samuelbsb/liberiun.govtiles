# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToCatalogBrain
from collective.cover import _

from liberiun.govtiles.models.searchterms import SearchTerms

class IMoreSearchTermsTile(IPersistentCoverTile):
    """
    """
    
    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )
    

class MoreSearchTermsTile(PersistentCoverTile):
    is_configurable = True


    def get_dados(self):
        """ Obtem os dados que serão usados no template
        """
        
        folder_context = self.context.aq_parent
        
        terms_obj = SearchTerms().getTopTermsByUID(folder_context.UID())
        terms = []
        
        if terms_obj:
            for term in terms_obj:
                terms.append(term.value);
        
        return {
            'title': self.data.get('title', None),
            'title_htmltag': self.get_tile_configuration()['title']['htmltag'],
            'list': terms
        }
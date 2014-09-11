# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToCatalogBrain
from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
from collective.cover import _
import json

from liberiun.govtiles.models.searchterms import SearchTerms

class IMoreSearchTermsTile(IPersistentCoverTile):
    """
    """
    
class MoreSearchTermsTile(PersistentCoverTile):
    is_configurable = True
    
    @property
    def portal_catalog(self):
        return self.context.portal_catalog

    def get_dados(self):
        """ Obtem os dados que serão usados no template
        """
        terms = []

        if self.hasSearchTileContext():
            folder_context = self.context.aq_parent
            portal = getUtility(ISiteRoot)
            terms_obj = SearchTerms().getTopTermsByUID(folder_context.UID())
            
            terms = []
            url_tile = ''
            
            tile = self.getSearchTileContext()
            url_tile = '@@{0}/{1}'.format(tile.get('tile-type'), tile.get('id'))
            
            if terms_obj:
                for term in terms_obj:
                    terms.append({'value':term.value,
                                  'url': "%s?submitted=submitted&SearchableText=%s" % (url_tile, term.value),
                                  'ajax_id': 'results-%s' % tile.get('id')});
        return {
            'list': terms
        }
        
    def getSearchTileContext(self):
        layout_dict = json.loads(self.context.cover_layout)
        tiles = []
        for row in layout_dict:
            row = row['children']
            for col in row:
                tiles += (col['children'])
        
        for tile in tiles:
            if tile.get('tile-type') == 'searchcontents':
                return tile
        return False
        
    
    def hasSearchTileContext(self):
        if self.getSearchTileContext():
            return True
        return False
# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.app.portlets.portlets.rss import RSSFeed

# store the feeds here (which means in RAM)
FEED_DATA = {}  # url: ({date, title, url, itemlist})

class IRSSFeedTile(IPersistentCoverTile):
    ''' '''
    
    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)
    
    url = schema.TextLine(title=_(u'URL of RSS feed'),
                        description=_(u'Link of the RSS feed to display.'),
                        required=True,
                        default=u'')


class RSSFeedTile(PersistentCoverTile):
    is_configurable = True
    
    def get_dados(self):
        ''' Obtem dados usados no template '''        
        return {
            'list': self._get_items()
        }
        
    def _get_items(self):
        items = []
        feed = self._get_feed()
        if feed:             
            items = feed.items[:self._get_count()]
        return items
    
    def _get_timeout(self):
        return 10
    
    def _get_url(self):
        return self.data.get('url', None)
    
    def _get_count(self):
        return self.data.get('count', None)
    
    def _get_feed(self):
        url = self._get_url()
        feed = FEED_DATA.get(url, None)
        if not feed:
            feed = FEED_DATA[url] = RSSFeed(url, self._get_timeout())
        feed.update()        
        return feed
# -*- coding: utf-8 -*-
from liberiun.govtiles.testing import INTEGRATION_TESTING
from liberiun.govtiles.tiles.rssfeed import RSSFeedTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest

URL = 'http://news.google.com.br/news?pz=1&cf=all&ned=pt-BR_br&hl=pt-BR&output=rss'
COUNT = 4


class RSSFeedTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u"rssfeed"
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(RSSFeedTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, RSSFeedTile))

        tile = RSSFeedTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_rss_render(self):
        self.tile.data['url'] = URL
        self.tile.data['count'] = COUNT
        dados = self.tile.get_dados()

        self.assertEqual(self.tile._get_url(), URL)
        self.assertEqual(self.tile._get_count(), COUNT)
        self.assertEqual(self.tile._get_timeout(), 10)
        self.assertEqual(len(dados['list']), COUNT)

# -*- coding: utf-8 -*-
from liberiun.govtiles.testing import INTEGRATION_TESTING
from liberiun.govtiles.tiles.sharing import SharingTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest

PLUGINS = ['twitter', 'facebook', 'gplus']


class SharingTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u"sharing"
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(SharingTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, SharingTile))

        tile = SharingTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_helper_utility(self):
        self.assertFalse(callable(self.tile.helper))

    def test_plugins(self):
        plugins_id = [i['id'] for i in self.tile.plugins()]
        for id in plugins_id:
            self.assertIn(id, PLUGINS)

# -*- coding: utf-8 -*-
from liberiun.govtiles.testing import INTEGRATION_TESTING
from liberiun.govtiles.tiles.iframe import IframeTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest

REMOTE_URL = 'http://www.liberiun.com'
HEIGHT = '400'


class IframeTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u"iframe"
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(IframeTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, IframeTile))

        tile = IframeTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertTrue(self.tile.is_editable)

    def test_iframe_render(self):
        self.tile.data['remote_url'] = REMOTE_URL
        self.tile.data['height'] = HEIGHT

        self.assertEqual(self.tile.getRemoteUrl(), REMOTE_URL)
        self.assertEqual(self.tile.getHeight(), HEIGHT)

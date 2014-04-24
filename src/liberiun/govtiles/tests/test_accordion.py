# -*- coding: utf-8 -*-
from liberiun.govtiles.testing import INTEGRATION_TESTING
from liberiun.govtiles.tiles.accordion import AccordionTile
from collective.cover.tiles.base import IPersistentCoverTile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.verify import verifyClass
from zope.interface.verify import verifyObject

import unittest


class AccordionTileTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.request = self.layer['request']
        self.name = u"accordion"
        self.cover = self.portal['frontpage']
        self.tile = getMultiAdapter((self.cover, self.request), name=self.name)
        self.tile = self.tile['test']

    def test_interface(self):
        self.assertTrue(IPersistentCoverTile.implementedBy(AccordionTile))
        self.assertTrue(verifyClass(IPersistentCoverTile, AccordionTile))

        tile = AccordionTile(None, None)
        self.assertTrue(IPersistentCoverTile.providedBy(tile))
        self.assertTrue(verifyObject(IPersistentCoverTile, tile))

    def test_default_configuration(self):
        self.assertFalse(self.tile.is_configurable)
        self.assertTrue(self.tile.is_droppable)
        self.assertFalse(self.tile.is_editable)

    def test_accepted_content_types(self):
        self.assertEqual(self.tile.accepted_ct(), ['Folder'])

    def test_accordion_render(self):
        folder = self.portal['my-folder1']
        accordions = ['My SubFolder1', 'My SubFolder2']
        self.tile.populate_with_object(folder)
        sub_list = self.tile.get_dados()['list']
        sub_titles = [i['title'] for i in sub_list]
        self.assertEqual(sub_titles, accordions)

# -*- coding: utf-8 -*-

from liberiun.govtiles.config import PROJECTNAME
from liberiun.govtiles.testing import INTEGRATION_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.browserlayer.utils import registered_layers
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

from Products.ResourceRegistries.config import CSSTOOLNAME, JSTOOLNAME

import unittest


DEPENDENCIES = [
    'collective.cover',
    'sc.social.like',
]

TILES = [
    'accordion',
    'iframe',
    'listfoldercontents',
    'rssfeed',
    'sharing',
    'bannerexterno',
]


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.ctool = self.portal[CSSTOOLNAME]
        self.jtool = self.portal[JSTOOLNAME]

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME), '%s not installed' % PROJECTNAME)

#    def test_dependencies(self):
#        for p in DEPENDENCIES:
#            self.assertTrue(self.qi.isProductInstalled(p),
#                '%s not installed' % p)

    def test_browserlayer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('ILiberiunGovTiles', layers, 'browser layer not installed')

    def test_tiles(self):
        self.registry = getUtility(IRegistry)
        registered_tiles = self.registry['plone.app.tiles']
        for tile in TILES:
            self.assertIn(tile, registered_tiles)

    def test_css_installed(self):
        installedStylesheetIds = self.ctool.getResourceIds()
        expected = ['++resource++liberiun.govtiles/liberiun_govtiles.css', ]
        for e in expected:
            self.assertTrue(e in installedStylesheetIds, e)

    def test_js_installed(self):
        installedScriptIds = self.jtool.getResourceIds()
        expected = ['++resource++liberiun.govtiles/liberiun_govtiles.js', ]
        for e in expected:
            self.assertTrue(e in installedScriptIds, e)


class UninstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.ctool = self.portal[CSSTOOLNAME]
        self.jtool = self.portal[JSTOOLNAME]

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME), '%s not uninstalled' % PROJECTNAME)

    def test_browserlayer_removed(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('ILiberiunGovTiles', layers, 'browser layer not removed')

    def test_css_removed(self):
        installedStylesheetIds = self.ctool.getResourceIds()
        expected = ['++resource++liberiun.govtiles/liberiun_govtiles.css', ]
        for e in expected:
            self.assertTrue(e not in installedStylesheetIds, e)

    def test_js_removed(self):
        installedScriptIds = self.jtool.getResourceIds()
        expected = ['++resource++liberiun.govtiles/liberiun_govtiles.js', ]
        for e in expected:
            self.assertTrue(e not in installedScriptIds, e)

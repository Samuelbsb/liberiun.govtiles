# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.cover
        self.loadZCML(package=collective.cover)
#        if 'virtual_hosting' not in app.objectIds():
#            # If ZopeLite was imported, we have no default virtual
#            # host monster
#            from Products.SiteAccess.VirtualHostMonster\
#            import manage_addVirtualHostMonster
#            manage_addVirtualHostMonster(app, 'virtual_hosting')
        import liberiun.govtiles
        self.loadZCML(package=liberiun.govtiles)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.cover:default')
        self.applyProfile(portal, 'collective.cover:testfixture')
        self.applyProfile(portal, 'liberiun.govtiles:default')
        self.applyProfile(portal, 'liberiun.govtiles:testfixture')

        # reindex objects to update catalog
        folder1 = portal['my-folder1']
        folder1.reindexObject()
        myfolder1 = folder1['my-subfolder1']
        myfolder1.reindexObject()
        myfolder2 = folder1['my-subfolder2']
        myfolder2.reindexObject()


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='liberiun.govtiles:Integration',
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='liberiun.govtiles:Functional',
)

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='liberiun.govtiles:Robot',
)

# -*- coding: utf-8 -*-

from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToObject,uuidToCatalogBrain
from Products.CMFCore.interfaces import IFolderish


class IAccordionTile(IPersistentCoverTile):
    ''' '''

    uuid = schema.TextLine(
        title=u'UUID',
        required=False,
        readonly=True,
    )


class AccordionTile(PersistentCoverTile):
    is_configurable = True

    @property
    def portal_catalog(self):
        return self.context.portal_catalog

    def populate_with_object(self, obj):
        '''
            Fará o set do uuid do objeto recebido por drag drop
        '''
        super(AccordionTile, self).populate_with_object(obj)
                
        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)
        data_mgr.set({'uuid': uuid})
        
        if hasattr(obj,'getCor') and callable(obj.getCor):
            cor = obj.getCor()
            conf = self.get_tile_configuration()
            conf.update({
                'css_class' : cor
            })
            self.set_tile_configuration(conf)

    def get_uuid_object(self):
        '''
            Obtem o brain do objeto cujo attr uuid faz referencia.
        '''
        uuid = self.data.get('uuid', None)
        if uuid:
            return uuidToCatalogBrain(uuid)

    def get_dados(self):
        '''
            Obtem os dados que serão usados no template
        '''
        folder = self.get_uuid_object()

        filhos = []
        if folder:
            filhos = self.get_childrens_brain(folder)

        return {
            'list' : (self._subeixo_for_dict(brain) for brain in filhos)
        }

    def get_childrens_brain(self, brain):
        '''
            Obtem os filhos de um objeto folder apartir de seu brain sem trazer os excluidos da navegacao
        '''
        brains = self.portal_catalog(path={'query':brain.getPath(),'depth':1})
        return (brain for brain in brains if not brain.exclude_from_nav)

    def _subeixo_for_dict(self ,brain):
        '''
            Converte um brain de um objeto folder em dicionario
        '''
        pages = (self._page_for_dict(page) for page in self.get_childrens_brain(brain))
        return {
            'title' : brain.Title,
            'pages' : pages
        }

    def _page_for_dict(self, brain):
        '''
            Converte uma pagina em dicionario
        '''
        url = brain.getURL()
        obj = brain.getObject()
        try:
            image = obj.restrictedTraverse(brain.getPath()+ "/@@images/icone/icon")
        except:
            image = None
        if image:
            return {
                'title' : brain.Title,
                'exclude_from_nav': brain.exclude_from_nav,
                'url' : url,
                'icone_url' : url + "/@@images/icone/icon"
            }
        else:
            return {
                'title' : brain.Title,
                'exclude_from_nav': brain.exclude_from_nav,
                'url' : url,
                'icone_url' : None
            }

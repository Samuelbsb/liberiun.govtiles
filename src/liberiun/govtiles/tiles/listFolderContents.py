# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToCatalogBrain


class IListFolderContentsTile(IPersistentCoverTile):
    """
    """

    uuid = schema.TextLine(
        title=u'UUID',
        required=False,
        readonly=True,
    )


class ListFolderContentsTile(PersistentCoverTile):
    is_configurable = True

    @property
    def portal_catalog(self):
        return self.context.portal_catalog

    def populate_with_object(self, obj):
        """ Fará o set do uuid do objeto recebido por drag drop
        """
        super(ListFolderContentsTile, self).populate_with_object(obj)
        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)
        data_mgr.set({'uuid': uuid})

    def get_uuid_object(self):
        """ Obtem o brain do objeto cujo attr uuid faz referencia.
        """
        uuid = self.data.get('uuid', None)
        if uuid:
            return uuidToCatalogBrain(uuid)

    def get_dados(self):
        """ Obtem os dados que serão usados no template
        """
        folder = self.get_uuid_object()

        filhos = []
        if folder:
            filhos = self.get_childrens_brain(folder)

        return {
            'list': [self._page_for_dict(brain) for brain in filhos]
        }

    def get_childrens_brain(self, brain):
        """ Obtem os filhos de um objeto folder apartir de seu brain sem trazer os excluidos da navegacao
        """
        brains = self.portal_catalog(path={'query': brain.getPath(), 'depth': 1})
        return (brain for brain in brains if not brain.exclude_from_nav)

    def _page_for_dict(self, brain):
        '''
            Converte uma pagina em dicionario
        '''
        return {
            'title': brain.Title,
            'url': brain.getURL(),
        }

# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.uuid.utils import uuidToCatalogBrain, uuidToObject
from collective.cover.widgets.textlinessortable import TextLinesSortableFieldWidget
from plone.autoform import directives as form
from collective.cover import _

from liberiun.govtiles.models.accesspage import AccessPage


FILE_CONTENT_TYPES = {
    'PDF' : ['application/pdf', 'application/x-pdf', 'image/pdf'],
    'DOC' : ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    'PPT' : ['application/vnd.ms-powerpoint', 'application/powerpoint', 'application/mspowerpoint', 'application/x-mspowerpoint'],
    'XLS' : ['application/vnd.ms-excel', 'application/msexcel', 'application/x-msexcel'],
}


types_display = SimpleVocabulary(
    [SimpleTerm(value=u'more_access', title=_(u'Mais acessados')),
     SimpleTerm(value=u'recent', title=_(u'Recentes')),
     SimpleTerm(value=u'featured', title=_(u'Destaques'))]
    )

content_types = SimpleVocabulary(
    [SimpleTerm(value=u'File', title=_(u'Arquivos')),
     SimpleTerm(value=u'BoaPratica', title=_(u'Boas Práticas')),]
    )

class IPagedCarouselTile(IPersistentCoverTile):
    """
    """
    
    title = schema.TextLine(
        title=_(u'Title'),
        required=True,
    )
    
    type_display = schema.Choice(
        title=_(u'Critério de exibição'),
        vocabulary=types_display,
        required=True,
    )
    
    content_type = schema.Choice(
        title=_(u'Tipo de conteúdo'),
        vocabulary=content_types,
        required=True,
    )
    
#     form.widget(uuids=TextLinesSortableFieldWidget)
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
        readonly=False,
    )

class PagedCarouselTile(PersistentCoverTile):
    is_configurable = True
    
    @property
    def portal_catalog(self):
        return self.context.portal_catalog
    
    def accepted_ct(self):
        """ Returna uma lista com os conteudos aceitos no tile
        """
        return ['Folder' , 'File', 'BoaPratica']
    
    def populate_with_object(self, obj):
        super(PagedCarouselTile, self).populate_with_object(obj)  # check permission
        
        type_display = self.data.get('type_display', None)
        content_type = self.data.get('content_type', None)
        
        if (type_display in ['more_access', 'recent'] and obj.portal_type != 'Folder') \
           or (type_display == 'featured' and obj.portal_type != content_type):
            raise Unauthorized(
                _('You are not allowed to add content to this tile'))
        
        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)

        old_data = data_mgr.get()
        if data_mgr.get()['uuids']:
            uuids = data_mgr.get()['uuids']
            if type(uuids) != list:
                uuids = [uuid]
            elif uuid not in uuids:
                uuids.append(uuid)
            old_data['uuids'] = uuids
        else:
            old_data['uuids'] = [uuid]
        data_mgr.set(old_data)
        
    def get_related_brains(self):
        """ Obtem o brain do objeto cujo attr uuid faz referencia.
        """
        uuids = self.data.get('uuids', None)
        brains = []
        
        if uuids:
            for uuid in uuids:
                brains.append(uuidToCatalogBrain(uuid))
            
        return brains
    
    def get_childrens_brain_by_type(self, brain, content_type):
        """ Obtem os filhos de um objeto folder apartir de seu brain
        """
        brains = self.portal_catalog(path={'query': brain.getPath(), 'depth': 1}, portal_type=content_type)
        return (brain for brain in brains)

    def get_dados(self):
        """ Obtem os dados que serão usados no template
        """
        
        type_display = self.data.get('type_display', None)
        content_type = self.data.get('content_type', None)
        
        if type_display == 'featured':
            brains = self.get_related_brains()
        else:
            brains = []
            folders = self.get_related_brains()
            for folder in folders:
                brains += self.get_childrens_brain_by_type(folder, content_type)
                
        if brains:
            if type_display == 'more_access':
                brains.sort(key=lambda l: AccessPage().getAmountAccessByUid(l.UID), reverse=True)
            elif type_display == 'recent':
                brains.sort(key=lambda l: l.created, reverse=True)
            
        
        return {
            'title': self.data.get('title', None),
            'type_display': type_display,
            'content_type': content_type,
            'title_htmltag': self.get_tile_configuration()['title']['htmltag'],
            'list': [self._brain_for_dict(brain) for brain in brains if brain]
        }
        
    def _brain_for_dict(self, brain):
        '''
            Converte uma pagina em dicionario
        '''
        data_object =  {
            'title': brain.Title,
            'url': brain.getURL()+'/view',
            'created': brain.created.strftime('%d/%m/%Y'),
            'portal_type': brain.portal_type,
            'access': AccessPage().getAmountAccessByUid(brain.UID),
        }
        
        if brain.portal_type == 'File':
            object = brain.getObject()
            data_object['file_size'] = brain.getObjSize
            
            #Define e extensao do arquivo baseado no content_type do OBJ
            file_meta_type = object.file.contentType
            file_type = ''
            for type in FILE_CONTENT_TYPES:
                if file_meta_type in FILE_CONTENT_TYPES[type]:
                    file_type = type
            if not file_type:
                file_type = 'TXT'
            data_object['content_type'] = file_type
            data_object['generic_type'] = 'CARTILHA'
            
        elif brain.portal_type == 'BoaPratica':
            object = brain.getObject()
            data_object['generic_type'] = object.getOrgaoresponsavel()
            
        
        return data_object
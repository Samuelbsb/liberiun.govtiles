# -*- coding: utf-8 -*-
from DateTime import DateTime
from collective.cover import _
from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from liberiun.govtiles.models.searchterms import SearchTerms


FILE_CONTENT_TYPES = {
    'PDF' : ['application/pdf', 'application/x-pdf', 'image/pdf'],
    'DOC' : ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    'PPT' : ['application/vnd.ms-powerpoint', 'application/powerpoint', 'application/mspowerpoint', 'application/x-mspowerpoint'],
    'XLS' : ['application/vnd.ms-excel', 'application/msexcel', 'application/x-msexcel'],
}

portal_types = SimpleVocabulary(
    [
     SimpleTerm(value=u'ArquivoBiblioteca', title=_(u'Arquivos Biblioteca')),
     SimpleTerm(value=u'BoaPratica', title=_(u'Boas Práticas')),]
    )

class ISearchContentsTile(IPersistentCoverTile):
    """
    """
    
    portal_type_selected = schema.Choice(
        title=_(u'Tipo de conteúdo'),
        vocabulary=portal_types,
        required=True,
    )
    
class SearchContentsTile(PersistentCoverTile):
    is_configurable = True
    
    @property
    def portal_catalog(self):
        return self.context.portal_catalog
    
    def get_dados(self):
        """ Obtem os dados que serão usados no template
        """
        
        portal_type_selected = self.data.get('portal_type_selected', None)
        all_subjects = self.portal_catalog.uniqueValuesFor('Subject')
        brains = []
        request = self.request
        form = request.form
        
        folder_context = self.context.aq_parent

        #Pega o contexto do portal
        portal_context = self.context.portal_url.getPortalObject()
        
        results = {}
        
        if portal_type_selected:
            query = {'path': {'query': '/'.join(portal_context.getPhysicalPath()), 'depth': 99},
                     'portal_type': portal_type_selected,}
            
            if form.get('submitted', False):
                indexes =  self.portal_catalog.indexes()

                for field, value in form.items():
                    if (field in indexes or 'date-' in field) and value:
                        
                        if field == 'SearchableText':
                            SearchTerms().manageSearchTerms(**{'value': value,
                                                               'uid': folder_context.UID(),
                                                               'type_object': portal_type_selected})
                            value = '*%s*' % form[field]
                        elif 'date-' in field:
                            date, index, field = field.split('-')
                            if not query.get(index, False):
                                str_input = '%s-%s-' % (date, index)
                                end = form.get(str_input+'end', DateTime() + 0.1) 
                                start = form.get(str_input+'start', DateTime() - 1)
                                
                                if end: end = DateTime(end) + 1
                                if start: start = DateTime(start)

                                if start and end:
                                    query_range = { 'query':(start,end), 'range': 'min:max'}
                                elif not end and start:
                                    query_range = { 'query':start, 'range': 'min'}
                                elif not start and end:
                                    query_range = { 'query':end, 'range': 'max'}

                                query[index] = query_range
                                
                            continue
                        else:
                            if field == 'Subject':
                                value= form[field]
                            else:
                                value = form[field].decode('utf-8')
                        
                        query[field] = value
            brains = self.portal_catalog(query)
        
        
        results = {
            'portal_type_selected': portal_type_selected,
            'list': [self._brain_for_dict(brain) for brain in brains if brain],
            'all_subjects': all_subjects,
        }
        
        if portal_type_selected == 'BoaPratica':
            results['all_orgaoresponsavel'] = self.portal_catalog.uniqueValuesFor('orgaoresponsavel')
        
        return results
        
    def _brain_for_dict(self, brain):
        '''
            Converte uma pagina em dicionario
        '''
        data_object =  {
            'title': brain.Title,
            'url': brain.getURL()+'/view',
            'created': brain.created.strftime('%d/%m/%Y'),
        }
        
        if brain.portal_type == 'ArquivoBiblioteca':
            object = brain.getObject()
            data_object['file_size'] = brain.getObjSize
            
            #Define e extensao do arquivo baseado no content_type do OBJ
            file_meta_type = object.getContentType()
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
# coding: utf-8

#Imports regarding the connection of the database 'storm'
from storm.locals import *
from storm.expr import *

from liberiun.govtiles.models.base import BaseStore

class SearchTerms(Storm, BaseStore):
    __storm_table__ = 'lib_govtiles_searchterms'
    
    value = Unicode()
    uid_object = Unicode()
    type_object = Unicode()
    amount_of_search = Int()
     
    def manageSearchTerms(self, **kwargs):
        """
            Método que gerencia os termos buscados no tile de busca, 
            caso o objeto já exista ele aumenta uma "busca" caso contrário ele cria um novo registro
            
            param: dicionario de dados contendo o termo, o UID do Tile e o Tipo do Conteudo da Busca
            ret: registro banco de dados
        """
        
        uid = kwargs.get('uid', '')
        value = kwargs.get('value', '')
        
        if value and uid:
            if not isinstance(uid, unicode):
                uid = uid.decode('utf-8')
            if not isinstance(value, unicode):
                value = value.decode('utf-8')
            
            term_obj = self.getSearchUniqueObjTerm(value, uid)
            
            if term_obj:
                amount = term_obj.amount_of_search
                term_obj.amount_of_search = amount + 1
            else:
                D={}
                D['value'] = value
                D['uid_object'] = uid
                D['type_object'] = kwargs.get('type_object', '').decode('utf-8')
                D['amount_of_search'] = 1
                
                term_obj = SearchTerms(**D)
                self.store.add(term_obj)
    
            self.store.flush()
            return term_obj
        
        return None

    def getSearchUniqueObjTerm(self, value, uid):
        """
            Retorna um registro de acordo com o UID buscado,
            caso não exista retorna nulo
            
            params: Valor do termo buscado
                    UID do objeto
            ret: registro unico do banco de dados
        """
        
        if not isinstance(uid, unicode):
            uid = uid.decode('utf-8')
        if not isinstance(value, unicode):
            value = value.decode('utf-8')
        
        data = self.store.find(SearchTerms,
                               SearchTerms.value == value,
                               SearchTerms.uid_object == uid,)
        
        if data.count() > 0:
            return data[0]
        else:
            return None
        
    
    def getTopTermsByUID(self, uid, total=10):
        """
            Retorna os termos mais buscados de acordo com o UID do objeto
            
            
            params: uid - UID do objeto
                    total - quantidade maxima de termos
            ret: registros mais buscados
        """
        
        if not isinstance(uid, unicode):
            uid = uid.decode('utf-8')
        
        data = self.store.find(SearchTerms,
                               SearchTerms.uid_object == uid,).order_by(Desc(SearchTerms.amount_of_search))[:total]
        
        if data.count() > 0:
            return data
        else:
            return None
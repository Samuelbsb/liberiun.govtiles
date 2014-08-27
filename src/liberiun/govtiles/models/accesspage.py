# coding: utf-8

#Imports regarding the connection of the database 'storm'
from storm.locals import *

from liberiun.govtiles.models.base import BaseStore

class AccessPage(Storm, BaseStore):
    __storm_table__ = 'lib_govtiles_accesspage'
    
    content_type = Unicode()
    uid = Unicode()
    amount_of_access = Int()
     
    def manageAccessPage(self, obj):
        """
            Método que gerencia os registros de acesso aos conteúdos, 
            caso o objeto já exista ele aumenta um "acesso" caso contrário ele cria um novo registro
            
            param: objeto plone
            ret: registro banco de dados
        """
        
        uid = obj.UID().decode('utf-8')
        
        access = self.getAccessObjByUid(uid)
        
        if access:
            amount = access.amount_of_access
            access.amount_of_access = amount + 1
        else:
            D={}
            D['content_type'] = obj.portal_type.decode('utf-8')
            D['uid'] = uid
            D['amount_of_access'] = 1 
            access = AccessPage(**D)
            self.store.add(access)

        self.store.flush()
        return access

    def getAccessObjByUid(self, uid):
        """
            Retorna um registro de acordo com o UID buscado,
            caso não exista retorna nulo
            
            param: UID do objeto
            ret: registro banco de dados
        """
        
        if not isinstance(uid, unicode):
            uid = uid.decode('utf-8')
        
        data = self.store.find(AccessPage, AccessPage.uid == uid)
        
        if data.count() > 0:
            return data[0]
        else:
            return None
        
    def getAmountAccessByUid(self, uid):
        """
            Retorna a quantidade de acessdos de um objeto a partir do UID,
            caso não exista retorna nulo
            
            param: UID do objeto
            ret: quantidade de acessos do objeto
        """
        
        data = self.getAccessObjByUid(uid)
        if data: 
            return data.amount_of_access
        
        return None
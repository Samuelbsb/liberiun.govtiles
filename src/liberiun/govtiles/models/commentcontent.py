# coding: utf-8

#Imports regarding the connection of the database 'storm'
from storm.locals import *
from storm.expr import *

from datetime import datetime

from liberiun.govtiles.models.base import BaseStore

from enum import Enum

class Status(Enum):
    pendente = 1
    aprovado = 2
    reprovado = 3

class CommentContent(Storm, BaseStore):
    __storm_table__ = 'lib_govtiles_commentcontent'
    
    uid = Unicode()
    username = Unicode()
    name = Unicode()
    email = Unicode()
    text = Unicode()
    status = Int() #Pendente, Aprovado, Reprovado
    date_status = DateTime()
    
    
    def newCommentContent(self, **kwargs):
        """
            
            @param **kwargs: dicionario de dados contendo - uid - UID do objeto
                                                            username - username de quem comentou
                                                            text - texto comentado no objeto
                                                            name - nome completo do comentador
                                                            email - email do comentador
            @return: registro novo cadastrado
        """
        
        uid = kwargs.get('uid', '')
        text = kwargs.get('text', '')
        username = kwargs.get('username', '')
        name = kwargs.get('name', '')
        email = kwargs.get('email', '')
        
        if uid and username and name and email:
            uid = self.convertToUTF(uid)
            text = self.convertToUTF(text)
            username = self.convertToUTF(username)
            name = self.convertToUTF(name)
            email = self.convertToUTF(email)
            
            D={'uid': uid,
               'username': username,
               'name': name,
               'email': email,
               'text': text,
               'status': Status.pendente.value,
               'date_status': datetime.now()}
            
            comment = CommentContent(**D)
            self.store.add(comment)

            self.store.flush()
            return comment
        
        return None
        
    def getCommentsByUID(self, uid):
        """
            Retorna os registros relacionados a um objeto
            
            @param uid: UID do objeto
            @return: DataSet do Storm com os registros de comentarios
        """
        
        uid = self.convertToUTF(uid)

        data = self.store.find(CommentContent,
                               CommentContent.uid == uid,
                               CommentContent.deleted == False).order_by(Desc(CommentContent.date_status))

        if data.count() > 0:
            return data
        else:
            return []
        
    def getCommentsByStatus(self, uid, status=Status.pendente):
        """
            Retorna os registros por status relacionados a um objeto
            
            @param uid: UID do objeto
            @param [data]: Parametro opcional caso já tenha um DataSet faço a busca em cima do mesmo
            @param [status]: Valor do campo status dos comentários
             
            @return: DataSet do Storm com os registros de comentarios
        """
        
        uid = self.convertToUTF(uid)

        data = self.store.find(CommentContent,
                               CommentContent.uid == uid,
                               CommentContent.status == status.value,
                               CommentContent.deleted == False).order_by(Desc(CommentContent.date_status))
        
        if data.count() > 0:
            return data
        else:
            return []
        
    def getPendingComments(self, uid):
        """
            Retorna os registros pendentes relacionados a um objeto
            
            @param uid: UID do objeto
            
            @return: DataSet do Storm com os registros de comentarios
        """
        
        return self.getCommentsByStatus(uid, Status.pendente)
    
    def getApprovedComments(self, uid):
        """
            Retorna os registros pendentes relacionados a um objeto
            
            @param uid: UID do objeto
            
            @return: DataSet do Storm com os registros de comentarios
        """
        
        return self.getCommentsByStatus(uid, Status.aprovado)
    
    def getDisapprovedComments(self, uid):
        """
            Retorna os registros pendentes relacionados a um objeto
            
            @param uid: UID do objeto
            
            @return: DataSet do Storm com os registros de comentarios
        """
        
        return self.getCommentsByStatus(uid, Status.reprovado)
    
    def getHistoryComments(self, uid):
        """
            Retorna os registros aprovados e reprovados menos os pendentes
            
            @param uid: UID do objeto
            
            @return: DataSet do Storm com os registros de comentarios
        """
        
        uid = self.convertToUTF(uid)

        data = self.store.find(CommentContent,
                               CommentContent.uid == uid,
                               Or(CommentContent.status == Status.aprovado.value, CommentContent.status == Status.reprovado.value) ,
                               CommentContent.deleted == False).order_by(Desc(CommentContent.date_status))
        
        if data.count() > 0:
            return data
        else:
            return []
        
    def changeStatus(self, ids, status):
        """
            Altera o status de uma lista de comentários
            
            @param ids: Lista com os ids (int) dos comentarios
            @param status: Status para qual os comentarios vao ser mudados
        """
        
        if not isinstance(ids, list):
            ids = list(ids)
        
        data = self.store.find(CommentContent,
                               CommentContent.id.is_in(ids),
                               CommentContent.deleted == False)
        
        for item in data:
            if item.status != status.value:
                item.status = status.value
                item.date_status = datetime.now()
            
        self.store.flush()
        
    def getNameStatus(self):
        return Status(self.status).name
    
            
            
            
             
        
        
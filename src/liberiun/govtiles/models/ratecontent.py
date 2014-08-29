# coding: utf-8

#Imports regarding the connection of the database 'storm'
from storm.locals import *
from storm.expr import *

from liberiun.govtiles.models.base import BaseStore

class RateContent(Storm, BaseStore):
    __storm_table__ = 'lib_govtiles_ratecontent'
    
    uid = Unicode()
    username = Unicode()
    rate = Unicode()
    
    def manageRateContent(self, **kwargs):
        """
            
            param: dicionario de dados contendo - uid - UID do objeto
                                                  username - username de quem votou
                                                  rate - valor da avaliação
            ret: registro banco de dados
        """
        
        uid = kwargs.get('uid', '')
        rate = kwargs.get('rate', '')
        username = kwargs.get('username', '')
        
        if rate and uid and username:
            uid = self.convertToUTF(uid)
            rate = self.convertToUTF(rate)
            username = self.convertToUTF(username)
            
            rate_obj = self.getRateContentByUsername(uid, username)
            
            if rate_obj:
                rate_obj.rate = rate
            else:
                D={}
                D['uid'] = uid
                D['username'] = username
                D['rate'] = rate

                rate_obj = RateContent(**D)
                self.store.add(rate_obj)

            self.store.flush()
            return rate_obj
        
        return None

    def getRateContentByUsername(self, uid, username):
        """

            params: uid - UID do objeto
                    username - username do usuario
                    
            ret: registro unico do banco de dados
        """
        
        uid = self.convertToUTF(uid)
        username = self.convertToUTF(username)

        data = self.store.find(RateContent,
                               RateContent.uid == uid,
                               RateContent.username == username,
                               RateContent.deleted == False)
        
        if data.count() > 0:
            return data[0]
        else:
            return None
        
    
    def getContentAvg(self, uid):
        """
            Retorna a média de avaliações de determinado conteúdo
            Caso necessario a média é arredondada para cima ou para baixo de acordo com a casa depois da virgula
            
            
            params: uid - UID do objeto a ser avaliado
            
            ret: valor da média,
                 quantidade de avaliações
        """
        
        uid = self.convertToUTF(uid)
        data = self.store.find(RateContent,
                               RateContent.uid == uid,
                               RateContent.deleted == False)
        
        if data.count() > 0:
            avg = 0
            sum = 0
            count = 0
            for item in data:
                item_rate = item.rate
                
                try:
                    item_rate = int(item_rate)
                    sum += item_rate
                    count += 1
                except:
                    continue
            avg = sum/count
            
            return avg, count
        else:
            return 0, 0
# coding: utf-8


#Imports regarding the connection of the database 'storm'
from storm.locals import *
from storm.zope.interfaces import IZStorm
from zope.component import getUtility
from datetime import datetime


#import sys
#from storm.tracer import debug #debug(True, stream=sys.stdout)

class BaseStore(object):
    
    id = Int(primary=True)
    deleted = Bool(default=False)
    date_created = DateTime(default=datetime.now())
    date_modified = DateTime(default=datetime.now())
    date_excluded = DateTime(default=datetime(1970,1,1,0,0,0))

    def __init__(self, *args, **kwargs):
        self.store = getUtility(IZStorm).get('govtiles_DB')

        #Lazy initialization of the object
        for attribute, value in kwargs.items():
            if not hasattr(self, attribute):
                raise TypeError('unexpected argument %s' % attribute)
            else:
                setattr(self, attribute, value)

        # divide o dicionario 'convertidos'
        for key in kwargs:
            setattr(self,key,kwargs[key])

        # adiciona a data atual
        self.date_created = datetime.now()
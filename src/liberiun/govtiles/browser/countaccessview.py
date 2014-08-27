# -*- coding: utf-8 -*-
from zope.interface import Interface
from Products.Five import BrowserView

from liberiun.govtiles.models.accesspage import AccessPage

class CountAccessView(BrowserView):
    """ 
    """
    
    def __call__(self):
        """
            Método de inicialização da view
        """
        
        self._computeAccess(self.context)
        return None
    
    def _computeAccess(self, obj):
        """
            Grava os dados do objeto no banco de dados gerando um acesso
        """
        
        access = AccessPage().manageAccessPage(obj)
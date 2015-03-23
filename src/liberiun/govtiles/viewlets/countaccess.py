# coding: utf-8

# Zope imports
from Acquisition import aq_inner
from zope.interface import Interface
from five import grok
from zope.component import getMultiAdapter

# Plone imports
from plone.app.layout.viewlets.interfaces import IAboveContent

# The viewlets in this file are rendered on every content item type
grok.context(Interface)

# Use templates directory to search for templates.
grok.templatedir('templates')

class CountAccessPage(grok.Viewlet):
    """ Essa viewlet vai contar os acessos a determinado tipo de conteúdo e gravar no BD """
    
    grok.viewletmanager(IAboveContent)
    
    def available(self):
        """ 
            Chece se o conteúdo acessado é para ser computado o acesso. 
        """
        
        if self.context.portal_type in ['ArquivoBiblioteca', 'BoaPratica']:
            return True
        else:
            return False
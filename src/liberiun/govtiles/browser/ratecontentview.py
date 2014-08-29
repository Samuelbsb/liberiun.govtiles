# -*- coding: utf-8 -*-
from zope.interface import Interface
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from liberiun.govtiles.models.ratecontent import RateContent


class RateContentView(BrowserView):
    """
    
    """
    
    index = ViewPageTemplateFile("ratecontentview.pt")
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        self.p_membership = context.portal_membership
    
    def __call__(self):
        uid = self.context.UID()
        username = self.p_membership.getAuthenticatedMember().getUserName()
        
        if username == 'Anonymous User':
            self.my_rate = 0
            self.is_anonymous = True
        else:
            my_rate = RateContent().getRateContentByUsername(uid, username)
            if my_rate and my_rate.rate:
                self.my_rate = my_rate.rate
            else:
                self.my_rate = 0
            self.is_anonymous = False
            
        self.content_avg, self.qtd_rate = RateContent().getContentAvg(uid)
        return self.index()
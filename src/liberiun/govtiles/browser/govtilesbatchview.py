# -*- coding: utf-8 -*-
from zope.interface import Interface
from ZTUtils import make_query
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.batching.browser import BatchView


class GovTilesBatchView(BatchView):
    """ 
    """
    
    index = ViewPageTemplateFile("navigationgovtiles.pt")
    
    def __call__(self, batch, batchformkeys=None, minimal_navigation=False, ajaxcontentid='content-batch'):
        super(GovTilesBatchView, self).__call__(batch, batchformkeys, minimal_navigation)
        self.ajaxcontentid = ajaxcontentid
        return self.index()
        
    
    def make_link(self, pagenumber=None):
        form = self.request.form
        
        if self.batchformkeys:
            batchlinkparams = dict([(key, form[key])
                                    for key in self.batchformkeys
                                    if key in form])
        else:
            batchlinkparams = form.copy()

        start = max(pagenumber - 1, 0) * self.batch.pagesize
        return '%s?%s' % (self.request.ACTUAL_URL, make_query(batchlinkparams,
                         {self.batch.b_start_str: start}))
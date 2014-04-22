# -*- coding: utf-8 -*-

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from zope.component._api import getMultiAdapter


class ISharingTile(IPersistentCoverTile):
    """
    """

class SharingTile(PersistentCoverTile):
    """ Baseado em sc.social.likes
    """
    
    enabled_portal_types = []
    typebutton = ''
    plugins_enabled = []
    render_method = 'plugin'
    
    @property
    def helper(self):
        return getMultiAdapter((self.context, self.request), name=u'sl_helper')
    
    def plugins(self):
        context = self.context
        render_method = self.render_method
        rendered = []
        plugins = self.helper.plugins()
        for plugin in plugins:
            if plugin and getattr(plugin, render_method)():
                view = context.restrictedTraverse(plugin.view())
                html = getattr(view, render_method)()
                rendered.append({'id': plugin.id,
                                 'html': html})
        return rendered
    
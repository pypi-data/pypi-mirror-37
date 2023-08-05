# -*- coding: utf-8 -*-
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from zope.component import getMultiAdapter
from plone import api


class IBandoDetailsPortlet(IPortletDataProvider):
    """A portlet displaying bando details
    """

class Assignment(base.Assignment):
    implements(IBandoDetailsPortlet)

    title = _(u'Bando details Portlet')


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('bando_details_portlet.pt')

    def render(self):
        return self._template()

    @property
    def available(self):
        context = self.context.aq_inner
        return context.portal_type == "Bando"

    def update(self):
        self.bando_view = getMultiAdapter(
            (self.context, self.request),
            name=u'bando_view')
        self.folder_deepenings = self.context.listFolderContents(
            contentFilter={"portal_type": 'Bando Folder Deepening'})

    def get_class_by_type(self, item):
        """
        return a css class based on filetype
        """
        if item.portal_type == "Link":
            return "linkItem"
        contenttype = ""
        try:
            contenttype = item.file.contentType
        except AttributeError:
            # Archetype
            contenttype = item.getFile().content_type
        if not contenttype:
            return ""
        if contenttype == "application/pdf":
            return "linkFilePdf"
        else:
            return "linkFile"

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()

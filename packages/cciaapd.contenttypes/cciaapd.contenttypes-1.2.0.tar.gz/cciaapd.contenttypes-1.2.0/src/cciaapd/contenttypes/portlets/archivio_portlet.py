from .. import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


class IArchivioPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=u"Titolo",
        required=True,
    )

    css_class = schema.TextLine(
        title=u"Classe css",
        required=False,
    )


class Assignment(base.Assignment):
    implements(IArchivioPortlet)

    def __init__(self, portlet_title, css_class):
        self.portlet_title = portlet_title
        self.css_class = css_class

    @property
    def title(self):
        return self.portlet_title


class AddForm(base.AddForm):
    form_fields = form.Fields(IArchivioPortlet)
    label = _(u"Add Archivio Portlet")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IArchivioPortlet)
    label = _(u"Edit Archivio Portlet")
    description = _(u"")


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('archivio_portlet.pt')

    def render(self):
        return self._template()

    @property
    def available(self):
        return self._data() is not None

    def getPortletClass(self):
        classes = "box boxScheda boxArchivio"
        if self.data.css_class:
            classes += " %s" % self.data.css_class
        return classes

    def results(self):
        return self._data()

    @memoize
    def _data(self):
        context = self.context.aq_inner
        if context.portal_type != 'Scheda':
            return None
        archivi = []
        for elem in context.aq_chain:
            try:
                elem_archivi = self.get_right_context(elem).listFolderContents(
                    contentFilter={'portal_type': "ArchivioFolder"}
                )
                for archivio in elem_archivi:
                    if archivio not in archivi and not archivio.isExpired():
                        archivi.append(archivio)
            except AttributeError:
                continue
        return archivi

    def get_right_context(self, item):
        ''' Check for default page and get it from the context
        if default page is not set return None, otherwise the object
        '''
        default_page_method = getattr(item, 'getDefaultPage', None)
        if not default_page_method:
            return item
        default_page = default_page_method()
        if not default_page:
            return item
        return item.get(default_page) or item

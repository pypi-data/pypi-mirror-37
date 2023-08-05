from .. import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


class IUfficioPortlet(IPortletDataProvider):

    portlet_title = schema.TextLine(
        title=u"Titolo",
        required=True,
    )

    css_class = schema.TextLine(
        title=u"Classe css",
        required=False,
    )


class Assignment(base.Assignment):
    implements(IUfficioPortlet)

    def __init__(self, portlet_title, css_class):
        self.portlet_title = portlet_title
        self.css_class = css_class

    @property
    def title(self):
        return self.portlet_title


class AddForm(base.AddForm):
    form_fields = form.Fields(IUfficioPortlet)
    label = _(u"Add Ufficio Portlet")
    description = _(u"")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IUfficioPortlet)
    label = _(u"Edit Ufficio Portlet")
    description = _(u"")


class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('ufficio_portlet.pt')

    def render(self):
        return self._template()

    @property
    def available(self):
        return len(self._data())

    def getPortletClass(self):
        classes = "box boxScheda boxOffice"
        if self.data.css_class:
            classes += " %s" % self.data.css_class
        return classes

    def results(self):
        return self._data()

    @memoize
    def _data(self):
        context = self.context.aq_inner
        if context.portal_type == 'Ufficio' or context == api.portal.get():
            return []

        view = getMultiAdapter(
            (context, self.request),
            name=u'ufficio_helper_view'
        )
        return view.get_results()

    def format_text_field(self, office, field):
        view = getMultiAdapter(
            (office, self.request),
            name=u'ufficio_view'
        )
        return view.html_to_text(getattr(office, field, ''))

    def generate_mail_tag(self, address):
        if not address:
            return ""
        tag = "<a title=\"%s\" href=\"javascript:location.href='"\
              "mailto:'+String.fromCharCode(" % address
        for index, letter in enumerate(address):
            tag += "%s" % ord(letter)
            if index + 1 < len(address):
                tag += ", "
        tag += ")+'?'\">%s</a>" % address
        return tag

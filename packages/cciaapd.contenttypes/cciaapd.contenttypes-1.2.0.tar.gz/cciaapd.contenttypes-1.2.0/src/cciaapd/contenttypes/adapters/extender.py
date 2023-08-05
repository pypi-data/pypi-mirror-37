# coding=utf-8
from .. import _
from Products.ATContentTypes.interface import IATContentType
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Archetypes.public import ReferenceField
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from cciaapd.contenttypes.interfaces import ICciaapdContenttypesLayer
from zope.component import adapts
from zope.interface import implements


class CustomReferenceField(ExtensionField, ReferenceField):
    """ A field, storing reference to an object """


class ContentTypeExtender(object):
    adapts(IATContentType)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    layer = ICciaapdContenttypesLayer

    _fields = [
        CustomReferenceField(
            "related_office",
            schemata="categorization",
            allowed_types=('Ufficio'),
            relationship='to_office',
            languageIndependent=True,
            multiValued=True,
            widget=ReferenceBrowserWidget(
                label=_(
                    u"label_related_office",
                    default=u"Related office"),
                ),
            ),
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields

# -*- coding: utf-8 -*-
from .. import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import alsoProvides
from ..interfaces import IUfficio
from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset


class IRelatedOffice(model.Schema):

    ''' Behavior interface
    '''
    form.widget(related_office=MultiContentTreeFieldWidget)

    related_office = RelationList(
        title=_(u'label_related_office', default=u'Related office'),
        default=[],
        value_type=RelationChoice(
            title=u"Related",
            source=ObjPathSourceBinder(
                object_provides=IUfficio.__identifier__),
        ),
        required=False
    )

fieldset = Fieldset('categorization',
                    label=_(u'Categorization'), fields=['related_office'])
IRelatedOffice.setTaggedValue(FIELDSETS_KEY, [fieldset])

class RelatedOffice(model.Schema):

    ''' Behavior interface
    '''

alsoProvides(IRelatedOffice, IFormFieldProvider)

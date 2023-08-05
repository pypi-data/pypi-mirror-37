# -*- coding: utf-8 -*-
from zope.interface import implementer
from interfaces import IScheda
from interfaces import IUfficio
from plone.dexterity.content import Container
from plone.dexterity.content import Item


@implementer(IScheda)
class Scheda(Container):

    """Convenience subclass for ``Collection`` portal type
    """


@implementer(IUfficio)
class Ufficio(Item):

    """Class for Ufficio """

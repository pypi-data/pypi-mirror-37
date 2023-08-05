from Products.CMFCore.utils import getToolByName
from plone.api.exc import InvalidParameterError
from .. import logger
from plone import api
from Products.CMFCore.interfaces import IFolderish


def notify_state_change(self, event):

    if not IFolderish.providedBy(self):
        return

    sublevels_list = self.listFolderContents()

    for item in sublevels_list:
        if item == self:
            continue
        if api.content.get_state(item) == 'published' and event.action == 'publish':
            continue
        if api.content.get_state(item) == 'private' and event.action == 'hide':
            continue
        if api.content.get_state(item) == 'visible' and event.action == 'reject':
            continue
        try:
            api.content.transition(item, transition=event.action)
        except InvalidParameterError as e:
            logger.exception(e)
        except Exception as e:
            logger.exception(e)

from Products.Five import BrowserView
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from OFS.interfaces import IOrderedContainer
from plone.memoize import view
from cciaapd.contenttypes import logger


class SchedeContentView(BrowserView):

    def get_position_in_parent(self, obj):
        """
        Use IOrderedContainer interface to extract the object's manual ordering position
        """
        parent = obj.aq_inner.aq_parent
        ordered = IOrderedContainer(parent, None)
        if ordered is not None:
            return ordered.getObjectPosition(obj.getId())
        return 0

    def sort_by_position(self, a, b):
        """
        Python list sorter cmp() using position in parent.

        Descending order.
        """
        return self.get_position_in_parent(a) - self.get_position_in_parent(b)

    def get_results(self, portal_type):
        """Returns results depending on request and the following logic

        Case 1: a folder with a Scheda set as  default view ->
                return scheda contents filtered by content_types

        Case 2: the context is a Scheda ->
                return the contents of Moduli or Riferimenti according
                to the requeste portal type

        Case 3: as a fallback return an empty list
        """
        if ISiteRoot.providedBy(self.context):
            return []
        if self.has_default_view(self.context):
            return self.find_nephews(portal_type,
                                     self.get_default_view_object(self.context))

        if self.is_scheda(self.context):
            return self.find_nephews(portal_type)
        return []

    @view.memoize
    def has_default_view(self, item):
        """Return true if the default view is set to Scheda"""
        obj = self.get_default_view_object(item)
        if not obj:
            return False
        return obj.portal_type == 'Scheda'

    @view.memoize
    def get_default_view_object(self, item):
        ''' Check for default page and get it from the context
        if default page is not set return None, otherwise the object
        '''
        default_page_method = getattr(item, 'getDefaultPage', None)
        if not default_page_method:
            return None
        default_page = default_page_method()
        obj = item.get(default_page)
        return obj

    def find_nephews(self, portal_type, context=None):
        '''
        Check inside objects all the filtered types and
        return their children.
        Moreover, parent folders must be traversed to get contents of the
        first one where the default view is set as Scheda, if exists.
        '''
        if context is None:
            context = self.context
        results = []
        schede_deep = 0
        for item in context.aq_chain:
            if schede_deep == 2:
                break
            context_state = getMultiAdapter(
                (item, self.request),
                name=u'plone_context_state'
            )
            if context_state.is_default_page():
                # if is a default view, skip it, we'll handle it on the folder.
                # this avoid double entries
                continue
            if not self.is_scheda(item) and not self.has_default_view(item):
                # if the context isn't a scheda and its default_view isn't a
                # scheda, skip it
                continue
            schede_attachments = self.get_scheda_attachments(item, portal_type)
            if schede_attachments:
                schede_deep = schede_deep + 1
                results.extend(schede_attachments)
        return results

    def get_scheda_attachments(self, scheda, portal_type):
        default_view_obj = self.get_default_view_object(scheda)
        if default_view_obj and self.is_scheda(default_view_obj):
            scheda = default_view_obj
        children = scheda.listFolderContents(
            contentFilter={'portal_type': portal_type})
        results = []
        for child in children:
            items = [x for x in child.listFolderContents() if not x.isExpired()]
            if items:
                results.extend(sorted(items, self.sort_by_position))
        return results

    def is_scheda(self, context):
        """Return true if the content is a Scheda"""
        return getattr(context, 'portal_type', "") == "Scheda"

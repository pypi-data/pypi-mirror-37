from Products.Five import BrowserView
from plone.dexterity.interfaces import IDexterityContent
from plone import api


class UfficioHelperView(BrowserView):

    def get_results(self):
        """
        Returns related offices depending on the type of current item (AT or DX).
        Omit expired offices
        """
        related_items = []
        if IDexterityContent.providedBy(self.context):
            related_items = [x.to_object for x in self.context.related_office]
        else:
            try:
                related_items_field = self.context.getField("related_office")
            except AttributeError:
                # context isn't a site content
                return []
            if related_items_field:
                related_items = related_items_field.get(self.context)
        if not related_items:
            return related_items
        return filter(self.can_view_item, related_items)

    def can_view_item(self, item):
        if not api.user.has_permission('View', obj=item):
            return False
        if item.isExpired():
            return False
        return True

    def __call__(self):
        """"""
        return self.get_results() or 'No results'

# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone import utils
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import PhysicalNavigationBreadcrumbs
from Products.CMFPlone.browser.navigation import get_view_url
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from zope.component import getMultiAdapter
from zope.interface import implements


class CustomBreadcrumbsView(PhysicalNavigationBreadcrumbs):
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        context = aq_inner(self.context)
        request = self.request
        container = utils.parent(context)

        name, item_url = get_view_url(context)
        if container is None:
            return (
                {'absolute_url': item_url,
                 'Title': utils.pretty_title_or_id(context, context), },
                )

        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())

        # Some things want to be hidden from the breadcrumbs
        if IHideFromBreadcrumbs.providedBy(context):
            return base

        if base:
            if container.portal_type == "Scheda" and utils.isDefaultPage(container, request):
                # if the parent is a Scheda and is set as default page, it
                # doesn't appears in the breadcrums, so we need to use context
                # absolute_url instead simple concatenation
                item_url = context.absolute_url()
            else:
                item_url = '%s/%s' % (base[-1]['absolute_url'], name)

        rootPath = getNavigationRoot(context)
        itemPath = '/'.join(context.getPhysicalPath())

        # don't show default pages in breadcrumbs or pages above the navigation
        # root
        if not utils.isDefaultPage(context, request) \
                and not rootPath.startswith(itemPath):
            base += (
                {'absolute_url': item_url,
                 'Title': utils.pretty_title_or_id(context, context), },
                )

        return base

# -*- coding: utf-8 -*-
from pkg_resources import get_distribution
from plone.app.blocks.interfaces import IBlocksTransformEnabled
from plone.memoize import view
from redturtle.tiles.management.browser import tiles_view
from zope.interface import implementer


@implementer(IBlocksTransformEnabled)
class SchedaTilesView(tiles_view.BaseView):
    """
    La vista specifica usata per le tile delle Schede (portal_type Scheda)
    """

    @property
    @view.memoize
    def pkg_version(self):
        return get_distribution("cciaapd.contenttypes").version

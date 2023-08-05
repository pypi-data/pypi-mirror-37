# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cciaapd.contenttypes.testing import CCIAAPD_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that cciaapd.contenttypes is properly installed."""

    layer = CCIAAPD_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cciaapd.contenttypes is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('cciaapd.contenttypes'))

    def test_browserlayer(self):
        """Test that ICciaapdContenttypesLayer is registered."""
        from cciaapd.contenttypes.interfaces import ICciaapdContenttypesLayer
        from plone.browserlayer import utils
        self.assertIn(ICciaapdContenttypesLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CCIAAPD_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cciaapd.contenttypes'])

    def test_product_uninstalled(self):
        """Test if cciaapd.contenttypes is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('cciaapd.contenttypes'))

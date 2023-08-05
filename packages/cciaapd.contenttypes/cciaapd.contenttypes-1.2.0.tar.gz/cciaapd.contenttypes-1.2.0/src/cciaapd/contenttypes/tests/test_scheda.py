# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from cciaapd.contenttypes.testing import CCIAAPD_CONTENTTYPES_INTEGRATION_TESTING  # noqa
from cciaapd.contenttypes.interfaces import IScheda

import unittest2 as unittest


class SchedaIntegrationTest(unittest.TestCase):

    layer = CCIAAPD_CONTENTTYPES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Scheda')
        schema = fti.lookupSchema()
        self.assertEqual(IScheda, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Scheda')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Scheda')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IScheda.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('Scheda', 'Scheda')
        self.assertTrue(
            IScheda.providedBy(self.portal['Scheda'])
        )

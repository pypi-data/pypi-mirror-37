# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cciaapd.contenttypes


class CciaapdContenttypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=cciaapd.contenttypes)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cciaapd.contenttypes:default')


CCIAAPD_CONTENTTYPES_FIXTURE = CciaapdContenttypesLayer()


CCIAAPD_CONTENTTYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CCIAAPD_CONTENTTYPES_FIXTURE,),
    name='CciaapdContenttypesLayer:IntegrationTesting'
)


CCIAAPD_CONTENTTYPES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CCIAAPD_CONTENTTYPES_FIXTURE,),
    name='CciaapdContenttypesLayer:FunctionalTesting'
)


CCIAAPD_CONTENTTYPES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CCIAAPD_CONTENTTYPES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CciaapdContenttypesLayer:AcceptanceTesting'
)

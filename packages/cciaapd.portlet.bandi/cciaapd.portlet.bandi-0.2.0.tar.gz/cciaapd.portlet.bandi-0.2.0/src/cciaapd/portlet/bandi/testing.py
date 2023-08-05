# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import cciaapd.portlet.bandi


class CciaapdPortletBandiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=cciaapd.portlet.bandi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'cciaapd.portlet.bandi:default')


CCIAAPD_PORTLET_BANDI_FIXTURE = CciaapdPortletBandiLayer()


CCIAAPD_PORTLET_BANDI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CCIAAPD_PORTLET_BANDI_FIXTURE,),
    name='CciaapdPortletBandiLayer:IntegrationTesting'
)


CCIAAPD_PORTLET_BANDI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CCIAAPD_PORTLET_BANDI_FIXTURE,),
    name='CciaapdPortletBandiLayer:FunctionalTesting'
)


CCIAAPD_PORTLET_BANDI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CCIAAPD_PORTLET_BANDI_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CciaapdPortletBandiLayer:AcceptanceTesting'
)

# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from cciaapd.portlet.bandi.testing import CCIAAPD_PORTLET_BANDI_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that cciaapd.portlet.bandi is properly installed."""

    layer = CCIAAPD_PORTLET_BANDI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if cciaapd.portlet.bandi is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('cciaapd.portlet.bandi'))

    def test_browserlayer(self):
        """Test that ICciaapdPortletBandiLayer is registered."""
        from cciaapd.portlet.bandi.interfaces import ICciaapdPortletBandiLayer
        from plone.browserlayer import utils
        self.assertIn(ICciaapdPortletBandiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = CCIAAPD_PORTLET_BANDI_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['cciaapd.portlet.bandi'])

    def test_product_uninstalled(self):
        """Test if cciaapd.portlet.bandi is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('cciaapd.portlet.bandi'))

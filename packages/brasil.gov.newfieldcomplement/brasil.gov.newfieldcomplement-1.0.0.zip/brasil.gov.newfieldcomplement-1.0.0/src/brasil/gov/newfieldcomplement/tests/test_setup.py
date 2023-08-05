# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from brasil.gov.newfieldcomplement.testing import BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that brasil.gov.newfieldcomplement is properly installed."""

    layer = BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if brasil.gov.newfieldcomplement is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'brasil.gov.newfieldcomplement'))

    def test_browserlayer(self):
        """Test that IBrasilGovNewfieldcomplementLayer is registered."""
        from brasil.gov.newfieldcomplement.interfaces import (
            IBrasilGovNewfieldcomplementLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IBrasilGovNewfieldcomplementLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['brasil.gov.newfieldcomplement'])

    def test_product_uninstalled(self):
        """Test if brasil.gov.newfieldcomplement is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'brasil.gov.newfieldcomplement'))

    def test_browserlayer_removed(self):
        """Test that IBrasilGovNewfieldcomplementLayer is removed."""
        from brasil.gov.newfieldcomplement.interfaces import \
            IBrasilGovNewfieldcomplementLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IBrasilGovNewfieldcomplementLayer,
            utils.registered_layers()
        )

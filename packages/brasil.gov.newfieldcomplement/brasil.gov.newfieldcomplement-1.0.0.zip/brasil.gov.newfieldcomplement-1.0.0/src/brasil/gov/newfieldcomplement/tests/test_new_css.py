# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement.testing import BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING
from plone import api

import unittest


class CssTest(unittest.TestCase):

    layer = BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.portal_css = api.portal.get_tool('portal_css')

    def test_css_registry(self):
        """ Verifica a inclusao do css no portal_css
        """
        ids = self.portal_css.getResourceIds()
        for css in [
            '++resource++brasil.gov.newfieldcomplement/bootstrap_table.css',
            '++resource++brasil.gov.newfieldcomplement/newfieldcomplement.css',
        ]:
            self.assertTrue(css in ids, u'CSS {0} not in portal_css.'.format(css))

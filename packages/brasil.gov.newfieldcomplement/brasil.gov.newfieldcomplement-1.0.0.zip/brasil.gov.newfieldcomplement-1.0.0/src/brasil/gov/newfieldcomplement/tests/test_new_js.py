# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement.testing import BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING
from plone import api

import unittest


class JsTest(unittest.TestCase):

    layer = BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.portal_javascripts = api.portal.get_tool('portal_javascripts')

    def test_js_registry(self):
        """ Verifica a inclusao do js no portal_javascripts
        """
        ids = self.portal_javascripts.getResourceIds()
        for js in [
            '++resource++brasil.gov.newfieldcomplement/newfieldcomplement.js',
        ]:
            self.assertTrue(js in ids, u'JS {0} not in portal_javascripts.'.format(js))

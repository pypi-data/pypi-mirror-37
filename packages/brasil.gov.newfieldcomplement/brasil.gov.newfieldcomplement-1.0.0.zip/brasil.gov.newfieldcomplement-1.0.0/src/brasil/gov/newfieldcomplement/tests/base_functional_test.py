# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from brasil.gov.newfieldcomplement.config import VOCABULARIES_REGISTRY_PREFIX
from brasil.gov.newfieldcomplement.testing import BRASIL_GOV_NEWFIELDCOMPLEMENT_FUNCTIONAL_TESTING
from brasil.gov.newfieldcomplement.testing import ADM
from brasil.gov.newfieldcomplement.testing import EDITOR
from brasil.gov.newfieldcomplement.testing import MANAGER
from brasil.gov.newfieldcomplement.testing import PASS
from eea.facetednavigation.interfaces import IDisableSmartFacets
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.interfaces import IHidePloneRightColumn
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.protect.utils import addTokenToUrl
from plone.protect.utils import createToken
from plone.testing.z2 import Browser
from StringIO import StringIO
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import os
import transaction
import unittest


class BaseFuncitonalTest(unittest.TestCase):

    layer = BRASIL_GOV_NEWFIELDCOMPLEMENT_FUNCTIONAL_TESTING

    def setUp(self):  # noqa
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        # Disable plone.protect for these tests
        self.request.form['_authenticator'] = createToken()
        # Eventuelly you find this also useful
        # self.request.environ['REQUEST_METHOD'] = 'POST'
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.view_name = ''
        self.portal_url = self.portal.absolute_url()

    def _login(self, rule='editor'):
        self.browser.open('{0}/login_form'.format(self.portal_url))
        if rule == 'editor':
            user = EDITOR
        elif rule == 'site administrator':
            user = ADM
        else:
            user = MANAGER
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = PASS
        self.browser.getControl(name='submit').click()

    def _control_panel(self):
        self.browser.open(
            addTokenToUrl(
                '{0}/@@overview-controlpanel'.format(
                    self.portal_url
                )
            )
        )

    def _save(self):
        self.browser.getControl(name='form.buttons.save').click()

    def _cancel(self):
        self.browser.getControl(name='form.buttons.cancel').click()

    def _open_relatorios(self):
        self.browser.open(
            addTokenToUrl('{0}/relatorios'.format(self.portal_url))
        )

    def _active_faceted(self):
        subtyper = getMultiAdapter(
            (self.portal['relatorios'], self.portal['relatorios'].REQUEST),
            name=u'faceted_subtyper'
        )
        subtyper.enable()
        search = getMultiAdapter(
            (self.portal['relatorios'], self.portal['relatorios'].REQUEST),
            name=u'faceted_search_subtyper'
        )
        search.enable()
        alsoProvides(self.portal['relatorios'], IFacetedNavigable)
        if not IDisableSmartFacets.providedBy(self.portal['relatorios']):
            alsoProvides(self.portal['relatorios'], IDisableSmartFacets)
        if not IHidePloneLeftColumn.providedBy(self.portal['relatorios']):
            alsoProvides(self.portal['relatorios'], IHidePloneLeftColumn)
        if not IHidePloneRightColumn.providedBy(self.portal['relatorios']):
            alsoProvides(self.portal['relatorios'], IHidePloneRightColumn)
        self._open_relatorios()
        self.browser.getLink(
            'Enable faceted navigation'
        ).click()
        self.browser.getControl(name='form.button.confirm').click()
        self.browser.getLink(
            'Enable faceted search'
        ).click()
        self.browser.getControl(name='form.button.confirm').click()
        transaction.commit()

    def _configure_faceted(self):
        exportimport = getMultiAdapter(
            (self.portal['relatorios'], self.portal['relatorios'].REQUEST),
            name=u'faceted_exportimport'
        )
        query = {
            'import_button': 'Import',
            'import_file': self._preparefile('../../../../../docs/relatorios.xml'),
            'redirect': '',
        }
        exportimport(**query)
        transaction.commit()

    def _active_faceted_tabular_view(self):
        self.browser.open(
            addTokenToUrl(
                '{}/relatorios/@@faceted_layout?layout=faceted-tabular-view'.format(
                    self.portal_url
                )
            )
        )
        # self.browser.getControl(name='form.button.confirm').click()
        transaction.commit()

    def _open_faceted_tabular_config(self):
        self.browser.open(
            addTokenToUrl(
                '{0}/relatorios/@@faceted-tabular-config'.format(
                    self.portal_url
                )
            )
        )

    def _configure_dynamic_vocabulary_01(self):
        api.portal.set_registry_record(
            name='{}.dynamic_vocabulary_01'.format(VOCABULARIES_REGISTRY_PREFIX),
            value=[
                u'Agricultura'
                u'Fazenda',
                u'Planejamento',
            ]
        )

    def _add_data_relatorio_index(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_catalog.manage_addIndex(
            name='data_relatorio',
            type='DateIndex',
            extra=None,
        )
        portal_catalog.addColumn(
            name='data_relatorio',
        )

    def _add_ministerio_relatorio_index(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        portal_catalog.manage_addIndex(
            name='ministerio_relatorio',
            type='FieldIndex',
            extra=None,
        )
        portal_catalog.addColumn(
            name='ministerio_relatorio',
        )

    def _test_anon(self):
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse(self.view_name)

    def _test_editor(self):
        logout()
        login(self.portal, EDITOR)
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse(self.view_name)

    def _loadfile(self, rel_filename):
        storage_path = os.path.join(os.path.dirname(__file__))
        file_path = os.path.join(storage_path, rel_filename)
        file_ob = open(file_path, 'rb')
        filedata = file_ob.read()
        filename = file_path.split('/')[-1]
        filename = str(filename)
        return {
            'name': filename,
            'data': filedata,
        }

    def _preparefile(self, rel_filename, ctype='text/xml'):
        ofile = self._loadfile(rel_filename)
        fp = StringIO(ofile.get('data'))
        fp.filename = ofile.get('name')
        return fp

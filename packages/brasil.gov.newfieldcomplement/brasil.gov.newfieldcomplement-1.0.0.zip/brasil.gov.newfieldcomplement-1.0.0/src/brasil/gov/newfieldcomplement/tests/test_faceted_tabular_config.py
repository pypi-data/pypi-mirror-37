# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement.tests.base_functional_test import BaseFuncitonalTest
from DateTime import DateTime
from plone import api
from plone.app.testing import logout

import transaction


class FacetedTabularConfigTest(BaseFuncitonalTest):

    def setUp(self):  # noqa
        super(FacetedTabularConfigTest, self).setUp()
        self.view_name = 'relatorios/@@faceted-tabular-config'
        self._configure_dynamic_vocabulary_01()
        self._add_data_relatorio_index()
        self._add_ministerio_relatorio_index()
        api.content.create(
            container=self.portal['relatorios'],
            type='File',
            id='arquivo-01',
            title=u'Arquivo 01',
            data_relatorio=DateTime('2018-07-29 00:00:00'),
            ministerio_relatorio='fazenda',
        )
        api.content.create(
            container=self.portal['relatorios'],
            type='File',
            id='arquivo-02',
            title=u'Arquivo 02',
            data_relatorio=DateTime('2018-07-30 00:00:00'),
            ministerio_relatorio='planejamento',
        )
        api.content.create(
            container=self.portal['relatorios'],
            type='File',
            id='arquivo-03',
            title=u'Arquivo 03',
            data_relatorio=DateTime('2018-07-31 00:00:00'),
            ministerio_relatorio='fazenda',
        )
        transaction.commit()

    def test_anon(self):
        self._test_anon()

    def test_editor(self):
        logout()
        self._login(rule='editor')
        self._active_faceted()
        self._configure_faceted()
        self._active_faceted_tabular_view()
        self.browser.open(
            '{}/relatorios/@@faceted-tabular-config'.format(self.portal_url)
        )
        self.assertTrue(
            'Faceted Tabular Fields'
            in self.browser.contents,
        )
        self.assertTrue(
            '<h1 class="documentFirstHeading">Faceted Tabular Fields</h1>'
            in self.browser.contents,
        )

    def test_admin(self):
        logout()
        self._login(rule='site administrator')
        self._active_faceted()
        self._configure_faceted()
        self._active_faceted_tabular_view()
        self.browser.open(
            '{}/relatorios/@@faceted-tabular-config'.format(self.portal_url)
        )
        self.assertTrue(
            'Faceted Tabular Fields'
            in self.browser.contents,
        )
        self.assertTrue(
            '<h1 class="documentFirstHeading">Faceted Tabular Fields</h1>'
            in self.browser.contents,
        )

    def test_column_and_title_completed(self):
        logout()
        self._login(rule='site administrator')
        self._active_faceted()
        self._configure_faceted()
        self._active_faceted_tabular_view()
        self.browser.open(
            '{}/relatorios/@@faceted-tabular-config'.format(self.portal_url)
        )
        self.browser.getControl(
            name='form.widgets.column_02:list',
        ).value = ['Description', ]
        self.browser.getControl(
            name='form.widgets.column_03:list',
        ).value = ['ministerio_relatorio', ]
        self._save()
        self.assertTrue(
            'Please fill in the title(s) of columns(s): 02, 03'
            in self.browser.contents
        )

    def test_at_least_a_link(self):
        logout()
        self._login(rule='site administrator')
        self._active_faceted()
        self._configure_faceted()
        self._active_faceted_tabular_view()
        self.browser.open(
            '{}/relatorios/@@faceted-tabular-config'.format(self.portal_url)
        )
        self.browser.getControl(
            name='form.widgets.column_01_link:list',
        ).value = []
        self._save()
        self.assertTrue(
            'Please select at least one column as a link to object view.'
            in self.browser.contents
        )

    def test_save(self):
        logout()
        self._login(rule='site administrator')
        self._active_faceted()
        self._configure_faceted()
        self._active_faceted_tabular_view()
        self.browser.open(
            '{}/relatorios/@@faceted-tabular-config'.format(self.portal_url)
        )
        self.browser.getControl(
            name='form.widgets.column_02:list',
        ).value = ['Description', ]
        self.browser.getControl(
            name='form.widgets.column_02_title',
        ).value = 'Descrição'
        self.browser.getControl(
            name='form.widgets.column_03:list',
        ).value = ['ministerio_relatorio', ]
        self.browser.getControl(
            name='form.widgets.column_03_vocab:list',
        ).value = ['brasil.gov.newfieldcomplement.dynamic_vocabulary_01', ]
        self.browser.getControl(
            name='form.widgets.column_03_title',
        ).value = 'Ministério'
        self.browser.getControl(
            name='form.widgets.column_04:list',
        ).value = ['data_relatorio', ]
        self.browser.getControl(
            name='form.widgets.column_04_title',
        ).value = 'Data'
        self.browser.getControl(
            name='form.widgets.column_05:list',
        ).value = ['getObjSize', ]
        self.browser.getControl(
            name='form.widgets.column_05_title',
        ).value = 'Tamanho'
        self._save()
        self.assertTrue(
            'Changes saved!'
            in self.browser.contents
        )
        transaction.commit()

    def test_cancel(self):
        logout()
        self._login(rule='site administrator')
        self._active_faceted()
        self._configure_faceted()
        self._active_faceted_tabular_view()
        self.browser.open(
            '{}/relatorios/@@faceted-tabular-config'.format(self.portal_url)
        )
        self.browser.getControl(
            name='form.widgets.column_02:list',
        ).value = ['Description', ]
        self.browser.getControl(
            name='form.widgets.column_02_title',
        ).value = 'Descrição'
        self._cancel()
        self.assertTrue(
            'Changes cancelled!'
            in self.browser.contents
        )

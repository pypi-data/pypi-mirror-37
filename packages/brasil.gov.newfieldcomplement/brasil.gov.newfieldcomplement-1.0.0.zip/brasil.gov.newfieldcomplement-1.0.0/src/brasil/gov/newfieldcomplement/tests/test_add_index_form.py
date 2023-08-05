# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from brasil.gov.newfieldcomplement.tests.base_functional_test import BaseFuncitonalTest
from plone.app.testing import logout


class AddIndexFormTest(BaseFuncitonalTest):

    def setUp(self):  # noqa
        super(AddIndexFormTest, self).setUp()
        self.view_name = '@@add-index-form'

    def test_anon(self):
        self._test_anon()

    def test_editor(self):
        self._test_editor()

    def test_adm(self):
        logout()
        self._login(rule='site administrator')
        self._control_panel()
        self.assertTrue(
            'Add portal_catalog Index'
            not in self.browser.contents
        )
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse(self.view_name)

    def _add_index_form(self):
        self._control_panel()
        self.browser.getLink(
            'Add portal_catalog Index'
        ).click()

    def _add(self):
        self.browser.getControl(name='form.buttons.add').click()

    def test_manager(self):
        logout()
        self._login(rule='manager')
        self._add_index_form()
        self.browser.getControl(
            name='form.widgets.short_field_name',
        ).value = 'new_field'
        self.browser.getControl(
            name='form.widgets.index_type:list',
        ).value = ['FieldIndex', ]
        self._add()
        self.assertTrue(
            'Index/metadata new_field successfully created.'
            in self.browser.contents
        )

    def test_there_are_index_metadata(self):
        logout()
        self._login(rule='manager')
        self._add_index_form()
        self.browser.getControl(
            name='form.widgets.short_field_name',
        ).value = 'review_state'
        self.browser.getControl(
            name='form.widgets.index_type:list',
        ).value = ['FieldIndex', ]
        self._add()
        self.assertTrue(
            'There are a index and a metadata with short name: review_state'
            in self.browser.contents
        )

    def test_there_is_index(self):
        logout()
        self._login(rule='manager')
        self._add_index_form()
        self.browser.getControl(
            name='form.widgets.short_field_name',
        ).value = 'SearchableText'
        self.browser.getControl(
            name='form.widgets.index_type:list',
        ).value = ['ZCTextIndex', ]
        self._add()
        self.assertTrue(
            'There is a index with short name: SearchableText'
            in self.browser.contents
        )

    def test_there_is_metadata(self):
        logout()
        self._login(rule='manager')
        self._add_index_form()
        self.browser.getControl(
            name='form.widgets.short_field_name',
        ).value = 'location'
        self.browser.getControl(
            name='form.widgets.index_type:list',
        ).value = ['FieldIndex', ]
        self._add()
        self.assertTrue(
            'There is a metadata with short name: location'
            in self.browser.contents
        )

    def test_short_field_name(self):
        logout()
        self._login(rule='manager')
        self._add_index_form()
        self.browser.getControl(
            name='form.widgets.short_field_name',
        ).value = 'get_field()'
        self.browser.getControl(
            name='form.widgets.index_type:list',
        ).value = ['FieldIndex', ]
        self._add()
        self.assertTrue(
            'Invalid short field name.'
            in self.browser.contents
        )

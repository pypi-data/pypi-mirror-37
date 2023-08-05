# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement.tests.base_functional_test import BaseFuncitonalTest
from plone.app.testing import logout


class DynamicVocabulariesFormTest(BaseFuncitonalTest):

    def setUp(self):  # noqa
        super(DynamicVocabulariesFormTest, self).setUp()
        self.view_name = '@@dynamic-vocabularies'

    def test_anon(self):
        self._test_anon()

    def test_editor(self):
        self._test_editor()

    def test_adm(self):
        logout()
        self._login(rule='site administrator')
        self._control_panel()
        self.browser.getLink('Dynamic Vocabularies').click()

        for i in range(1, 16):
            self.assertTrue(
                'Vocabulary {:02d}'.format(i) in self.browser.contents,
            )

            self.browser.getControl(
                name='form.widgets.dynamic_vocabulary_{:02d}'.format(i),
            ).value = '{}\n{}\n{}'.format(i, i + 1, i + 2)

        self._save()
        self.assertTrue(
            'Changes saved.' in self.browser.contents,
        )

    def test_unique(self):
        logout()
        self._login(rule='site administrator')
        self._control_panel()
        self.browser.getLink('Dynamic Vocabularies').click()

        self.browser.getControl(
            name='form.widgets.dynamic_vocabulary_05',
        ).value = '1\n2\n1'
        self._save()
        self.assertTrue('One or more entries of sequence are not unique.' in self.browser.contents)

    def test_cancel(self):
        logout()
        self._login(rule='site administrator')
        self._control_panel()
        self.browser.getLink('Dynamic Vocabularies').click()

        self.browser.getControl(
            name='form.widgets.dynamic_vocabulary_01',
        ).value = '4\n5\n6'
        self._cancel()
        self.assertTrue(
            'Changes canceled.' in self.browser.contents,
        )

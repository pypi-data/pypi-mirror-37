# -*- coding: utf-8 -*-

from datetime import date
from DateTime import DateTime
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class FacetedTabularView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.utils = getMultiAdapter(
            (self.context, self.request),
            name='newfieldcomplement_utils',
        )
        self.plone = getMultiAdapter(
            (self.context, self.request),
            name='plone',
        )

    def get_title_by_value(self, vocab_name=None, value=None):
        factory = getUtility(IVocabularyFactory, vocab_name)
        vocabulary = factory(self.context)
        if value:
            term = vocabulary.getTerm(value)
            return term.title
        return ''

    def get_faceted_tabular_fields(self):
        return self.utils.get_faceted_tabular_fields()

    def get_value(self, field_name=None, vocab_name=None, brain=None):
        if brain.has_key(field_name):  # noqa
            if isinstance(brain[field_name], date):
                return brain[field_name].strftime('%d/%m/%Y')
            elif isinstance(brain[field_name], DateTime):
                return self.plone.toLocalizedTime(
                    brain[field_name],
                    long_format=True,
                )
            elif field_name == 'Date' and isinstance(brain[field_name], str):
                return self.plone.toLocalizedTime(
                    DateTime(brain[field_name]),
                    long_format=True,
                )
            elif vocab_name is not None:
                return self.get_title_by_value(vocab_name, brain[field_name])
            return brain[field_name]
        return u''

    def get_url(self, brain):
        if brain['portal_type'] in self.utils.get_types_use_view():
            return '{0}/view'.format(brain.getURL())
        return brain.getURL()

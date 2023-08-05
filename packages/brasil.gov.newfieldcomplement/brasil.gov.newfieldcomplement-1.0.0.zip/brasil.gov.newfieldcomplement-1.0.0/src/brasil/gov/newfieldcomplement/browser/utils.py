# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from brasil.gov.newfieldcomplement.interfaces import IUtilsView
from plone import api
from plone.memoize.view import memoize
from zope.annotation.interfaces import IAnnotations
from zope.interface import implementer


@implementer(IUtilsView)
class UtilsView(BrowserView):
    """funcoes reutilizaveis"""

    def get_faceted_tabular_fields(self):
        """campos exibidos na visao facetada tabular"""
        annotations = IAnnotations(self.context)
        if 'faceted_tabular_fields' in annotations.keys():
            content = annotations['faceted_tabular_fields']
        else:
            content = {
                'column_01': u'Title',
                'column_01_title': u'Título',
                'column_01_link': True
            }
            for i in range(2, 6):
                content['column_{:02d}'.format(i)] = None
                content['column_{:02d}_vocab'.format(i)] = None
                content['column_{:02d}_title'.format(i)] = None
                content['column_{:02d}_link'.format(i)] = False
        return content

    @memoize
    def get_types_use_view(self):
        portal_properties = api.portal.get_tool(name='portal_properties')
        return getattr(
            portal_properties.site_properties,
            'typesUseViewActionInListings',
            ()
        )

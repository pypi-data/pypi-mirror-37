# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBrasilGovNewfieldcomplementLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IUtilsView(Interface):
    """funcoes reutilizaveis"""

    def get_faceted_tabular_fields(self):
        """campos exibidos na visao facetada tabular"""

    def get_types_use_view(self):
        """tipos que utilizam /view na url"""

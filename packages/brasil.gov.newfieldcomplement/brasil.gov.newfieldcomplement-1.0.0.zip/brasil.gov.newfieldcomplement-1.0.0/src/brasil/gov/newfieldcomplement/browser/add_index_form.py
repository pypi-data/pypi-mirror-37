# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement import _
from brasil.gov.newfieldcomplement.config import INDEX_TYPES
from plone.api import portal
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.z3cform.layout import wrap_form
from Products.ZCTextIndex.OkapiIndex import OkapiIndex
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.schema import ValidationError


class InvalidShortFieldName(ValidationError):
    __doc__ = _(u'Invalid short field name.')


def validate_short_field_name(value):
    for i in ('(', ')', '+', '*', '/', '\\', '<', '>', '%', '$', '\#', '&'):
        if value.find(i) != -1:
            raise InvalidShortFieldName(value)
    return True


class IAddIndexForm(Interface):

    short_field_name = schema.TextLine(
        title=_(u'Short field name or get function'),
        required=True,
        constraint=validate_short_field_name,
    )

    index_type = schema.Choice(
        title=_(u'Index Type'),
        vocabulary=u'brasil.gov.newfieldcomplement.index_types',
        default=None,
        missing_value=u'',
        required=True,
    )


class AddIndexForm(form.Form):

    label = _(u'Add portal_catalog Index')

    fields = field.Fields(IAddIndexForm)
    ignoreContext = True

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_catalog = portal.get_tool('portal_catalog')
        self.portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state',
        )

    def updateWidgets(self):
        super(AddIndexForm, self).updateWidgets()

    def _index_type(self, short_field_name, index_type):
        if index_type == 'ZCTextIndex':
            idx = INDEX_TYPES[index_type](
                id=short_field_name,
                caller=self.portal_catalog,
                index_factory=OkapiIndex,
                field_name=short_field_name,
                lexicon_id='htmltext_lexicon'
            )
        else:
            idx = INDEX_TYPES[index_type](id=short_field_name)
        return idx

    def _add_portal_catalog_index(self, short_field_name, idx):
            self.portal_catalog.manage_addIndex(
                name=short_field_name,
                type=idx,
                extra=None,
            )
            self.portal_catalog.addColumn(
                name=short_field_name,
            )
            self.portal_catalog.reindexIndex(
                name=[short_field_name, ],
                REQUEST=self.request,
            )

    def _display_message(self, message, type):
        portal.show_message(
            message,
            self.request,
            type=type,
        )

    def _redirect(self, view):
        redirect_url = '{0}/{1}'.format(
            self.portal_state.portal_url(),
            view,
        )
        self.request.response.redirect(redirect_url)

    @button.buttonAndHandler(_(u'Add'))
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            return

        indexes = self.portal_catalog.indexes()
        schema = self.portal_catalog.schema()

        short_field_name = data['short_field_name'].encode('utf-8')
        index_type = data['index_type']
        idx = self._index_type(short_field_name, index_type)

        if short_field_name not in indexes and short_field_name not in schema:
            self._add_portal_catalog_index(short_field_name, idx)
            self._display_message(
                _(
                    u'Index/metadata ${name} successfully created.',
                    mapping={'name': short_field_name},
                ),
                'info',
            )
            self._redirect('@@add-index-form')
        elif short_field_name in indexes and short_field_name in schema:
            self._display_message(
                _(
                    u'There are a index and a metadata with short name: ${name}',
                    mapping={'name': short_field_name},
                ),
                'error',
            )
            return
        elif short_field_name in indexes:
            self._display_message(
                _(
                    u'There is a index with short name: ${name}',
                    mapping={'name': short_field_name},
                ),
                'error',
            )
            return
        else:
            self._display_message(
                _(
                    u'There is a metadata with short name: ${name}',
                    mapping={'name': short_field_name},
                ),
                'error',
            )
            return

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self._display_message(
            _('Action canceled.'),
            'info',
        )
        self._redirect('@@overview-controlpanel')


AddIndexFormView = wrap_form(AddIndexForm, ControlPanelFormWrapper)

# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement import _
from brasil.gov.newfieldcomplement.config import VOCABULARIES_PREFIX
from persistent.dict import PersistentDict
from plone import api
from plone.directives.form import Schema
from plone.directives.form import SchemaForm
from plone.supermodel.model import fieldset
from z3c.form import button
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter


class IFacetedTabularConfigForm(Schema):
    """ Define form fields """

    fieldset(
        'column_01_fieldset',
        label=_(u'Column 01'),
        fields=[
            'column_01',
            'column_01_vocab',
            'column_01_title',
            'column_01_link',
        ]
    )
    column_01 = schema.Choice(
        title=_(u'Column 01'),
        required=True,
        default=u'Title',
        vocabulary='{}.available_fields'.format(VOCABULARIES_PREFIX)
    )
    column_01_vocab = schema.Choice(
        title=_(u'Column 01 Vocabulary'),
        required=False,
        vocabulary='eea.faceted.vocabularies.PortalVocabularies',
    )
    column_01_title = schema.TextLine(
        title=_(u'Column 01 Title'),
        required=True,
        default=u'Título',
    )
    column_01_link = schema.Bool(
        title=_(u'Column 01 Link'),
        required=False,
        default=True,
    )

    fieldset(
        'column_02_fieldset',
        label=_(u'Column 02'),
        fields=[
            'column_02',
            'column_02_vocab',
            'column_02_title',
            'column_02_link',
        ]
    )
    column_02 = schema.Choice(
        title=_(u'Column 02'),
        required=False,
        vocabulary='{}.available_fields'.format(VOCABULARIES_PREFIX)
    )
    column_02_vocab = schema.Choice(
        title=_(u'Column 02 Vocabulary'),
        required=False,
        vocabulary='eea.faceted.vocabularies.PortalVocabularies',
    )
    column_02_title = schema.TextLine(
        title=_(u'Column 02 Title'),
        description=_(u'title_description'),
        required=False,
    )
    column_02_link = schema.Bool(
        title=_(u'Column 02 Link'),
        required=False,
        default=False,
    )

    fieldset(
        'column_03_fieldset',
        label=_(u'Column 03'),
        fields=[
            'column_03',
            'column_03_vocab',
            'column_03_title',
            'column_03_link',
        ]
    )
    column_03 = schema.Choice(
        title=_(u'Column 03'),
        required=False,
        vocabulary='{}.available_fields'.format(VOCABULARIES_PREFIX)
    )
    column_03_vocab = schema.Choice(
        title=_(u'Column 03 Vocabulary'),
        required=False,
        vocabulary='eea.faceted.vocabularies.PortalVocabularies',
    )
    column_03_title = schema.TextLine(
        title=_(u'Column 03 Title'),
        description=_(u'title_description'),
        required=False,
    )
    column_03_link = schema.Bool(
        title=_(u'Column 03 Link'),
        required=False,
        default=False,
    )

    fieldset(
        'column_04_fieldset',
        label=_(u'Column 04'),
        fields=[
            'column_04',
            'column_04_vocab',
            'column_04_title',
            'column_04_link',
        ]
    )
    column_04 = schema.Choice(
        title=_(u'Column 04'),
        required=False,
        vocabulary='{}.available_fields'.format(VOCABULARIES_PREFIX)
    )
    column_04_vocab = schema.Choice(
        title=_(u'Column 04 Vocabulary'),
        required=False,
        vocabulary='eea.faceted.vocabularies.PortalVocabularies',
    )
    column_04_title = schema.TextLine(
        title=_(u'Column 04 Title'),
        description=_(u'title_description'),
        required=False,
    )
    column_04_link = schema.Bool(
        title=_(u'Column 04 Link'),
        required=False,
        default=False,
    )

    fieldset(
        'column_05_fieldset',
        label=_(u'Column 05'),
        fields=[
            'column_05',
            'column_05_vocab',
            'column_05_title',
            'column_05_link',
        ]
    )
    column_05 = schema.Choice(
        title=_(u'Column 05'),
        required=False,
        vocabulary='{}.available_fields'.format(VOCABULARIES_PREFIX)
    )
    column_05_vocab = schema.Choice(
        title=_(u'Column 05 Vocabulary'),
        required=False,
        vocabulary='eea.faceted.vocabularies.PortalVocabularies',
    )
    column_05_title = schema.TextLine(
        title=_(u'Column 05 Title'),
        description=_(u'title_description'),
        required=False,
    )
    column_05_link = schema.Bool(
        title=_(u'Column 05 Link'),
        required=False,
        default=False,
    )


class FacetedTabularConfigForm(SchemaForm):
    """ /@@faceted-tabular-config
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.utils = getMultiAdapter(
            (self.context, self.request),
            name='newfieldcomplement_utils',
        )

    schema = IFacetedTabularConfigForm
    ignoreContext = False

    label = _(u'Faceted Tabular Fields')

    def _display_message(self, message, type):
        api.portal.show_message(
            message,
            self.request,
            type=type,
        )

    def _validate_column_and_title_completed(self, data):
        errors = []
        for i in range(2, 6):
            column = 'column_{:02d}'.format(i)
            title = 'column_{:02d}_title'.format(i)
            if data[column] and not data[title]:
                errors.append('{:02d}'.format(i))
        return errors

    def _at_least_a_link(self, data):
        for i in range(1, 6):
            link = 'column_{:02d}_link'.format(i)
            if data[link]:
                return True
        return False

    def _set_data(self, data={}):
        annotations = IAnnotations(self.context)
        annotations['faceted_tabular_fields'] = PersistentDict(
            data
        )

    def getContent(self):
        return self.utils.get_faceted_tabular_fields()

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        data, errors = self.extractData()
        title_not_completed = self._validate_column_and_title_completed(data)
        if title_not_completed:
            self._display_message(
                _(
                    u'Please fill in the title(s) of columns(s): ${titles}',
                    mapping={
                        'titles': ', '.join(title_not_completed)
                    },
                ),
                'error',
            )
            return
        if not self._at_least_a_link(data):
            self._display_message(
                _(
                    u'Please select at least one column as a link to object view.'
                ),
                'error',
            )
            return
        if errors:
            self.status = self.formErrorsMessage
            return
        if data:
            self._set_data(data)
            self.status = _(u'Changes saved!')

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self._display_message(
            _(u'Changes cancelled!'),
            'info',
        )
        self.request.response.redirect(self.context.absolute_url())

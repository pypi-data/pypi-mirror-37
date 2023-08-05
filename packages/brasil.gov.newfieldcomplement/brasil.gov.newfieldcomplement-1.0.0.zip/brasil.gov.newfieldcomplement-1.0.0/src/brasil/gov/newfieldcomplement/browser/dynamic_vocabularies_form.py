# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement import _
from plone.app.registry.browser import controlpanel
from plone.supermodel.model import fieldset
from zope import schema
from zope.interface import Interface


class IDynamicVocabularies(Interface):

    fieldset(
        'vocabulary_01_fieldset',
        label=_(u'Vocabulary 01'),
        fields=[
            'dynamic_vocabulary_01',
        ]
    )
    dynamic_vocabulary_01 = schema.List(
        title=_(u'dynamic_vocabulary_01'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value')),
    )
    fieldset(
        'vocabulary_02_fieldset',
        label=_(u'Vocabulary 02'),
        fields=[
            'dynamic_vocabulary_02',
        ]
    )
    dynamic_vocabulary_02 = schema.List(
        title=_(u'dynamic_vocabulary_02'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_03_fieldset',
        label=_(u'Vocabulary 03'),
        fields=[
            'dynamic_vocabulary_03',
        ]
    )
    dynamic_vocabulary_03 = schema.List(
        title=_(u'dynamic_vocabulary_03'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_04_fieldset',
        label=_(u'Vocabulary 04'),
        fields=[
            'dynamic_vocabulary_04',
        ]
    )
    dynamic_vocabulary_04 = schema.List(
        title=_(u'dynamic_vocabulary_04'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_05_fieldset',
        label=_(u'Vocabulary 05'),
        fields=[
            'dynamic_vocabulary_05',
        ]
    )
    dynamic_vocabulary_05 = schema.List(
        title=_(u'dynamic_vocabulary_05'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_06_fieldset',
        label=_(u'Vocabulary 06'),
        fields=[
            'dynamic_vocabulary_06',
        ]
    )
    dynamic_vocabulary_06 = schema.List(
        title=_(u'dynamic_vocabulary_06'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_07_fieldset',
        label=_(u'Vocabulary 07'),
        fields=[
            'dynamic_vocabulary_07',
        ]
    )
    dynamic_vocabulary_07 = schema.List(
        title=_(u'dynamic_vocabulary_07'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_08_fieldset',
        label=_(u'Vocabulary 08'),
        fields=[
            'dynamic_vocabulary_08',
        ]
    )
    dynamic_vocabulary_08 = schema.List(
        title=_(u'dynamic_vocabulary_08'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_09_fieldset',
        label=_(u'Vocabulary 09'),
        fields=[
            'dynamic_vocabulary_09',
        ]
    )
    dynamic_vocabulary_09 = schema.List(
        title=_(u'dynamic_vocabulary_09'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_10_fieldset',
        label=_(u'Vocabulary 10'),
        fields=[
            'dynamic_vocabulary_10',
        ]
    )
    dynamic_vocabulary_10 = schema.List(
        title=_(u'dynamic_vocabulary_10'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_11_fieldset',
        label=_(u'Vocabulary 11'),
        fields=[
            'dynamic_vocabulary_11',
        ]
    )
    dynamic_vocabulary_11 = schema.List(
        title=_(u'dynamic_vocabulary_11'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_12_fieldset',
        label=_(u'Vocabulary 12'),
        fields=[
            'dynamic_vocabulary_12',
        ]
    )
    dynamic_vocabulary_12 = schema.List(
        title=_(u'dynamic_vocabulary_12'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_13_fieldset',
        label=_(u'Vocabulary 13'),
        fields=[
            'dynamic_vocabulary_13',
        ]
    )
    dynamic_vocabulary_13 = schema.List(
        title=_(u'dynamic_vocabulary_13'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_14_fieldset',
        label=_(u'Vocabulary 14'),
        fields=[
            'dynamic_vocabulary_14',
        ]
    )
    dynamic_vocabulary_14 = schema.List(
        title=_(u'dynamic_vocabulary_14'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )
    fieldset(
        'vocabulary_15_fieldset',
        label=_(u'Vocabulary 15'),
        fields=[
            'dynamic_vocabulary_15',
        ]
    )
    dynamic_vocabulary_15 = schema.List(
        title=_(u'dynamic_vocabulary_15'),
        description=_('dynamic_vocabulary_desc'),
        required=False,
        unique=True,
        value_type=schema.TextLine(title=_(u'Value'))
    )


class DynamicVocabulariesEditForm(controlpanel.RegistryEditForm):

    schema = IDynamicVocabularies
    label = _(u'Dynamic Vocabularies')
    description = _(u'')

    def update(self):
        super(DynamicVocabulariesEditForm, self).update()
        for idx, group in enumerate(self.groups, 1):
            widgets = group.widgets
            field = 'dynamic_vocabulary_{:02d}'.format(idx)
            widgets[field].rows = 10


class DynamicVocabulariesControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DynamicVocabulariesEditForm

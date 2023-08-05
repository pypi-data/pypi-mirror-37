# -*- coding: utf-8 -*-

from Products.PluginIndexes.BooleanIndex.BooleanIndex import BooleanIndex
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
from Products.PluginIndexes.KeywordIndex.KeywordIndex import KeywordIndex
from Products.ZCTextIndex.ZCTextIndex import ZCTextIndex


INDEX_TYPES = {
    u'BooleanIndex': BooleanIndex,
    u'DateIndex': DateIndex,
    u'FieldIndex': FieldIndex,
    u'KeywordIndex': KeywordIndex,
    u'ZCTextIndex': ZCTextIndex,
}


STATES = [
    u'',
    u'AC',
    u'AL',
    u'AP',
    u'AM',
    u'BA',
    u'CE',
    u'DF',
    u'ES',
    u'GO',
    u'MA',
    u'MT',
    u'MS',
    u'MG',
    u'PA',
    u'PB',
    u'PE',
    u'PI',
    u'PR',
    u'RJ',
    u'RN',
    u'RS',
    u'RO',
    u'RR',
    u'SC',
    u'SP',
    u'SE',
    u'TO'
]


VOCABULARIES_PREFIX = 'brasil.gov.newfieldcomplement'


VOCABULARIES_REGISTRY_PREFIX = 'brasil.gov.newfieldcomplement.browser.dynamic_vocabularies_form.IDynamicVocabularies'


DISABLED_METADATA_FIELDS = [
    'CreationDate',
    'Creator',
    'EffectiveDate',
    'ExpirationDate',
    'ModificationDate',
    'SearchableText',
    'Type',
    'UID',
    'author_name',
    'byline',
    'cmf_uid',
    'commentators',
    'exclude_from_nav',
    'getIcon'
    'getId',
    'getShowTitle',
    'in_response_to',
    'is_folderish',
    'last_comment_date',
    'listCreators',
    'meta_type',
    'portal_type',
    'review_state',
    'skos',
    'Subject',
    'sync_uid',
    'total_comments',
]

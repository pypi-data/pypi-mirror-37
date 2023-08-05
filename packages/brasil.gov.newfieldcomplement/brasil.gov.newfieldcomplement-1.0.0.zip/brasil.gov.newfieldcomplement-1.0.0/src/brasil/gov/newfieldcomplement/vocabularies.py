# -*- coding: utf-8 -*-

from brasil.gov.newfieldcomplement.config import DISABLED_METADATA_FIELDS
from brasil.gov.newfieldcomplement.config import INDEX_TYPES
from brasil.gov.newfieldcomplement.config import STATES
from brasil.gov.newfieldcomplement.config import VOCABULARIES_REGISTRY_PREFIX
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def _terms(items=[], normalize=False):
    normalizer = getUtility(IIDNormalizer)
    terms = []
    for item in items:
        if isinstance(item, str) or isinstance(item, unicode):
            value = normalize and normalizer.normalize(item) or item
            terms.append(
                SimpleTerm(
                    value=value,
                    token=value,
                    title=item
                )
            )
        else:
            terms.append(
                SimpleTerm(
                    value=item[0],
                    token=item[0],
                    title=item[1]
                )
            )
    return terms


def _get_registry_value(id):
    values = api.portal.get_registry_record(
        '{0}.{1}'.format(VOCABULARIES_REGISTRY_PREFIX, id)
    )
    if not values:
        values = [u'']
    return values


@implementer(IVocabularyFactory)
def available_fields_vocabulary(context):
    portal_catalog = api.portal.get_tool('portal_catalog')
    fields = [field for field in portal_catalog.schema() if field not in DISABLED_METADATA_FIELDS]
    return SimpleVocabulary(_terms(fields))


@implementer(IVocabularyFactory)
def states_vocabulary(context):
    return SimpleVocabulary(_terms(STATES))


@implementer(IVocabularyFactory)
def path_folders_vocabulary(context):
    paths = [
        brain.getPath()
        for brain in api.content.find(
            context=api.portal.get(), portal_type='Folder', sort_on='path'
        )
    ]
    return SimpleVocabulary(_terms(paths))


@implementer(IVocabularyFactory)
def index_types_vocabulary(context):
    return SimpleVocabulary(_terms(INDEX_TYPES.keys()))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_01(context):
    values = _get_registry_value('dynamic_vocabulary_01')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_02(context):
    values = _get_registry_value('dynamic_vocabulary_02')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_03(context):
    values = _get_registry_value('dynamic_vocabulary_03')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_04(context):
    values = _get_registry_value('dynamic_vocabulary_04')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_05(context):
    values = _get_registry_value('dynamic_vocabulary_05')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_06(context):
    values = _get_registry_value('dynamic_vocabulary_06')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_07(context):
    values = _get_registry_value('dynamic_vocabulary_07')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_08(context):
    values = _get_registry_value('dynamic_vocabulary_08')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_09(context):
    values = _get_registry_value('dynamic_vocabulary_09')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_10(context):
    values = _get_registry_value('dynamic_vocabulary_10')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_11(context):
    values = _get_registry_value('dynamic_vocabulary_11')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_12(context):
    values = _get_registry_value('dynamic_vocabulary_12')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_13(context):
    values = _get_registry_value('dynamic_vocabulary_13')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_14(context):
    values = _get_registry_value('dynamic_vocabulary_14')
    return SimpleVocabulary(_terms(values, True))


@implementer(IVocabularyFactory)
def dynamic_vocabulary_15(context):
    values = _get_registry_value('dynamic_vocabulary_15')
    return SimpleVocabulary(_terms(values, True))

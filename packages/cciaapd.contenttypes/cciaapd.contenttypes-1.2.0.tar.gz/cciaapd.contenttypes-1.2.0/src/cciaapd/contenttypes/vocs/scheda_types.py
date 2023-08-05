# -*- coding=utf-8 -*-
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


SCHEDA_TYPES = [
    (u'Moduli', 'ModuliFolder'),
    (u'Riferimenti', 'RiferimentiFolder'),
]

scheda_types = SimpleVocabulary([
    SimpleTerm(x[1], x[1], x[0])
    for x in SCHEDA_TYPES
])

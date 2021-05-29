import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.extractions import DependencyRelationshipExtract, \
                                   OneSidedRelationshipExtract
from eeyore_nlp.integrations import SpacyIntegration
from eeyore_nlp.models import Context

def test_extractor_1():
    context = Context(
        'Tom declined cancer treatment.',
        ['Tom', 'declined', 'cancer', 'treatment', '.']
    )
    context.add('entities', ['B-PER', '', 'B-dX', 'I-dX', ''])

    spacy = SpacyIntegration('en_core_web_lg')
    extract = DependencyRelationshipExtract(
        spacy=spacy,
        attribute='entities',
        e1='PER',
        e2='dX'
    )

    relationships = extract.evaluate(context)
    assert len(relationships) == 1

    kb_triple = relationships[0]
    assert kb_triple.rel == 'declined'
    assert kb_triple.subj == 'Tom'
    assert kb_triple.obj == 'cancer treatment'

def test_extractor_2():
    context = Context(
        'Declined cancer treatment.',
        ['Declined', 'cancer', 'treatment', '.']
    )
    context.add('entities', ['', 'B-dX', 'I-dX', ''])

    spacy = SpacyIntegration('en_core_web_lg')
    extract = OneSidedRelationshipExtract(
        spacy=spacy,
        attribute='entities',
        side_of_relation='e2',
        e1='PER',
        e2='dX'
    )

    relationships = extract.evaluate(context, 'Tom')
    assert len(relationships) == 1

    kb_triple = relationships[0]
    assert kb_triple.rel == 'Declined'
    assert kb_triple.subj == 'Tom'
    assert kb_triple.obj == 'cancer treatment'

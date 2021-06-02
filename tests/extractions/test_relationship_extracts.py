import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.extractions import DependencyRelationshipExtract, \
                                   OneSidedRelationshipExtract
from eeyore_nlp.integrations import SpacyIntegration
from eeyore_nlp.models import Context

def test_extractor_1():
    context = Context(
        'Tom and Bob declined cancer treatment.',
        ['Tom', 'and', 'Bob', 'declined', 'cancer', 'treatment', '.']
    )
    context.add('entities', ['B-A', '', 'B-A', '', 'B-B', 'B-C', ''])

    spacy = SpacyIntegration('en_core_web_lg')
    extract = DependencyRelationshipExtract(
        spacy=spacy,
        attribute='entities',
        relationships=[
            ('A', 'has_B', 'B'),
            ('B', 'has_C', 'C'),
        ]
    )

    relationships = extract.evaluate(context)
    assert len(relationships) == 2

    kb_triples = relationships[0]
    assert kb_triples[0].subj == 'Tom'
    assert kb_triples[0].obj == 'cancer'

    assert kb_triples[1].subj == 'cancer'
    assert kb_triples[1].obj == 'treatment'

    kb_triples = relationships[1]
    assert kb_triples[0].subj == 'Bob'
    assert kb_triples[0].obj == 'cancer'

    assert kb_triples[1].subj == 'cancer'
    assert kb_triples[1].obj == 'treatment'

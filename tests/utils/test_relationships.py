import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.utils import RelationshipBuilder
from eeyore_nlp.models import RelationshipKey

def test_relationship_builder():
    tokens = [
        'I',
        'am',
        'testing',
        'this',
        'class',
        '.'
    ]

    builder = RelationshipBuilder()
    rels = builder.create_neighbor_relationships(tokens)

    assert rels[0].primary == RelationshipKey('<start>')
    assert rels[0].children == [RelationshipKey('I')]

    assert rels[-2].primary == RelationshipKey('.')
    assert rels[-2].children == [RelationshipKey('<end>')]

    assert rels[-1].primary == RelationshipKey('<end>')

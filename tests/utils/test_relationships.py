import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.utils import RelationshipBuilder

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

    assert rels[0].primary == '<start>'
    assert rels[0].children == ['I']

    assert rels[-1].primary == '.'
    assert rels[-1].children == ['<end>']

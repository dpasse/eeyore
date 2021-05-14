import os
import sys
import pytest

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.models import Relationship, RelationshipKey

def test_relationship_addition():
    rel1 = Relationship(
        RelationshipKey('P1'),
        [RelationshipKey('C1')]
    )
    rel1 += Relationship(
        RelationshipKey('P1'),
        [RelationshipKey('C2'), RelationshipKey('C3')]
    )

    assert rel1.children == [
        RelationshipKey('C1'),
        RelationshipKey('C2'),
        RelationshipKey('C3')
    ]

def test_not_compatible_relationship_addition():
    rel1 = Relationship(
        RelationshipKey('P1'),
        [RelationshipKey('C1')]
    )
    with pytest.raises(ValueError):
        rel1 += Relationship(
            RelationshipKey('P2'),
            [RelationshipKey('C2'), RelationshipKey('C3')]
        )

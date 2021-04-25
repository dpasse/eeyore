import os
import sys
import pytest

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Relationship

def test_relationship_addition():
    rel1 = Relationship('P1', ['C1'])
    rel1 += Relationship('P1', ['C2', 'C3'])

    assert rel1.children == ['C1', 'C2', 'C3']

def test_not_compatible_relationship_addition():
    rel1 = Relationship('P1', ['C1'])
    with pytest.raises(ValueError):
        rel1 += Relationship('P2', ['C2', 'C3'])

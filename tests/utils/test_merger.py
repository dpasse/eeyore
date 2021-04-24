import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Context
from eeyore.utils import Merger

def test_combine():
    context = Context(
        'We are not going to New York.',
        ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']
    )
    context.add('entities', ['', '', '', '', '', 'LOC', 'LOC', ''])
    context.add('negatives', ['', '', 'NEG', '', '', '', '', ''])

    data = Merger.combine(
        context,
        ['tokens', 'entities', 'negatives']
    )

    assert data == [
        { 'tokens': 'We' },
        { 'tokens': 'are' },
        { 'tokens': 'not', 'negatives': 'NEG' },
        { 'tokens': 'going' },
        { 'tokens': 'to' },
        { 'tokens': 'New', 'entities': 'LOC' },
        { 'tokens': 'York', 'entities': 'LOC' },
        { 'tokens': '.' },
    ]

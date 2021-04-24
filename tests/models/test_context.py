import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Context

def test_context_add_and_get():
    context = Context('We are not going to New York.')
    context.add('entities', ['', '', '', '', '', 'LOC', 'LOC', ''])
    context.add('negatives', ['', '', 'NEG', '', '', '', '', ''])
    context.add('negative_scope', ['', '', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG'])

    assert len(context.keys) == 4
    assert len(context.get('tokens')) == 8
    assert len(context.get('entities')) == 8
    assert len(context.get('negatives')) == 8
    assert len(context.get('negative_scope')) == 8

def test_context_cache():
    context = Context('We are not going to New York.', actor='Tom', line=4, sent_number=3)
    assert context.cache['actor'] == 'Tom'
    assert context.cache['line'] == 4
    assert context.cache['sent_number'] == 3

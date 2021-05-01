import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.extractions import ScopeOverlapExtract
from eeyore_nlp.models import Context

def test_extractor_1():
    context = Context(
        'Tom declined cancer treatment.',
        ['Tom', 'declined', 'cancer', 'treatment', '.']
    )
    context.add('scope1', ['', 'S1', 'S1', 'S1', 'S1'])
    context.add('scope2', ['', '', 'S2', 'S2', ''])

    relationships = ScopeOverlapExtract('scope1', 'scope2').evaluate(context)

    assert relationships == ['', 'REL', 'REL', 'REL', 'REL']

def test_extractor_2():
    context = Context(
        'Tom declined cancer treatment.',
        ['Tom', 'declined', 'cancer', 'treatment', '.']
    )
    context.add('scope1', ['', 'S1', 'S1', '', ''])
    context.add('scope2', ['', '', 'S2', 'S2', ''])

    relationships = ScopeOverlapExtract('scope1', 'scope2').evaluate(context)
    assert relationships == ['', 'REL', 'REL', 'REL', '']

def test_extractor_3():
    context = Context(
        'Tom declined cancer treatment.',
        ['Tom', 'declined', 'cancer', 'treatment', '.']
    )
    context.add('scope1', ['S1', 'S1', '', '', ''])
    context.add('scope2', ['', '', '', 'S2', ''])

    relationships = ScopeOverlapExtract('scope1', 'scope2').evaluate(context)
    assert relationships == ['', '', '', '', '']

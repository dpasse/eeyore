import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.taggers import TreeChunker
from eeyore_nlp.models import Context

def test_chunker_single_term_phrase():
    chunker = TreeChunker("NP: {<DT>?<JJ>*<NN>}", attribute='pos')

    context = Context(
        'learn php from guru99',
        ['learn','php', 'from','guru99']
    )
    context.add('pos', ['JJ', 'NN', 'IN', 'NN'])

    chunks = chunker.tag(context)
    assert chunks == ['B-NP', 'I-NP', '', 'B-NP']

def test_chunker_single_term_phrase_not_pos():
    chunker = TreeChunker("AB: {<A><B>}", attribute='outer')

    context = Context(
        'learn php from guru99',
        ['learn','php', 'from','guru99']
    )
    context.add('outer', ['A', 'B', '', ''])

    chunks = chunker.tag(context)
    assert chunks == ['B-AB', 'I-AB', '', '']

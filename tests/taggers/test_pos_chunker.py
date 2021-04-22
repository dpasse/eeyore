import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.taggers import PosChunker
from eeyore.models import Context

def test_chuker_single_term_phrase():
    chunker = PosChunker("NP: {<DT>?<JJ>*<NN>}")

    context = Context('learn php from guru99')
    context.add('pos', ['JJ', 'NN', 'IN', 'NN'])

    chunks = chunker.tag(context)
    assert chunks == ['B-NP', 'I-NP', '', 'B-NP']

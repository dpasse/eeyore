import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Context

def test_chuker_single_term_phrase():
    context = Context(
        'We are not going to New York.',
        ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.'],
        **{
            'negatives': ['', '', 'NEG', '', '', '', '', '']
        }
    )

    assert len(context.get('tokens')) == 8
    assert len(context.get('negatives')) == 8

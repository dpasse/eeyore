import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Context

def test_chuker_single_term_phrase():
    context = Context(
        'We are not going to New York.',
        entities=['', '', '', '', '', 'LOC', 'LOC', ''],
        negatives=['', '', 'NEG', '', '', '', '', ''],
        negative_scope=['', '', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG']
    )

    assert len(context.keys) == 4
    assert len(context.get('tokens')) == 8
    assert len(context.get('entities')) == 8
    assert len(context.get('negatives')) == 8
    assert len(context.get('negative_scope')) == 8

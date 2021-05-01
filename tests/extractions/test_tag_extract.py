import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.extractions import TagExtract
from eeyore_nlp.models import Context

def test_extractor():
    context = Context(
        'We are not going to New York.',
        ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']
    )
    context.add('negative', ['', '', 'NEG', 'NEG', '', '', '', ''])
    context.add('negative_scope', ['', '', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG'])
    context.add('entities', ['', '', '', '', '', 'B-LOC', 'I-LOC', ''])

    negative_extracts = TagExtract('negative', ['NEG']).evaluate(context)
    negative_scope_extracts = TagExtract(
        'negative_scope',
        ['NEG']
    ).evaluate(context)
    location_extracts = TagExtract(
        'entities',
        ['LOC']
    ).evaluate(context)

    assert negative_extracts == {
        'NEG': [
            [
                (2, 'not'),
                (3, 'going')
            ],
        ]
    }

    assert negative_scope_extracts == {
        'NEG': [
            [
                (2, 'not'),
                (3, 'going'),
                (4, 'to'),
                (5, 'New'),
                (6, 'York'),
                (7, '.')
            ],
        ]
    }

    assert location_extracts == {
        'LOC': [
            [
                (5, 'New'),
                (6, 'York')
            ]
        ]
    }

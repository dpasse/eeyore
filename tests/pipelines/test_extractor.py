import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Tag, RegexPhrase, Scope, ScopeDirection
from eeyore.taggers import Chunker, Scoper
from eeyore.pipelines import ChunkerPipe, ScoperPipe, Extractor

def test_extracting_multiple_pipes():
    extractor = Extractor(
        pipes=[
            ChunkerPipe(
                'entities',
                Chunker(tags=[
                    Tag('LOC', phrase=RegexPhrase(r'\b(New York)\b')),
                ]),
                order=1
            ),
            ChunkerPipe(
                'neg',
                Chunker(tags=[
                    Tag('FRW-NEG', phrase=RegexPhrase(r'\b(not)\b')),
                ]),
                order=2
            ),
            ScoperPipe(
                'neg_scope',
                focus='neg',
                scoper=Scoper(
                    scopes=[
                        Scope(
                            applied_tag='FRW-NEG',
                            scope_direction=ScopeDirection.FORWARD,
                            order=1,
                        )
                    ],
                ),
                order=3,
            )
        ]
    )

    context = extractor.execute('We are not going to New York.')

    assert len(context.keys) == 4
    assert context.get('tokens') == [
        'We',
        'are',
        'not',
        'going',
        'to',
        'New',
        'York',
        '.'
    ]
    assert context.get('entities') == ['', '', '', '', '', 'LOC', 'LOC', '']
    assert context.get('neg') == ['', '', 'FRW-NEG', '', '', '', '', '']
    assert context.get('neg_scope') == [
        '',
        '',
        'FRW-NEG',
        'FRW-NEG',
        'FRW-NEG',
        'FRW-NEG',
        'FRW-NEG',
        'FRW-NEG',
    ]

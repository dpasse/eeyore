import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.models import Tag, RegexPhrase, Scope, ScopeDirection
from eeyore.taggers import PhraseChunker, Scoper
from eeyore.pipelines import ChunkerPipe, ScoperPipe, AttributePipe, Pipeline

def test_extracting_multiple_pipes():
    pipeline = Pipeline(
        pipes=[
            ChunkerPipe(
                'regex_ner',
                PhraseChunker(tags=[
                    Tag('LOC', phrase=RegexPhrase(r'\b(New York)\b')),
                ]),
                order=1
            ),
            AttributePipe(order=2),
            ChunkerPipe(
                'neg',
                PhraseChunker(tags=[
                    Tag('FRW-NEG', phrase=RegexPhrase(r'\b(not)\b')),
                ]),
                order=3
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
                order=4,
            )
        ]
    )

    context = pipeline.execute('We are not going to New York.')

    assert len(context.keys) == 5
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
    assert context.get('pos') == [
      'PRP', 'VBP', 'RB', 'VBG', 'TO', 'NNP', 'NNP', '.'
    ]
    assert context.get('regex_ner') == ['', '', '', '', '', 'LOC', 'LOC', '']
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

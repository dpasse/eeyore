import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.models import Tag, RegexPhrase, Scope, ScopeDirection, Context
from eeyore_nlp.taggers import PhraseChunker, Scoper
from eeyore_nlp.pipelines import ChunkerPipe, TokenTaggerPipe, TokenAttributesPipe, ContextPipeline

def test_extracting_multiple_pipes():
    pipeline = ContextPipeline(
        pipes=[
            TokenAttributesPipe(),
            ChunkerPipe(
                'regex_ner',
                PhraseChunker(tags=[
                    Tag('LOC', phrase=RegexPhrase(r'\b(New York)\b')),
                ]),
                order=2
            ),
            ChunkerPipe(
                'neg',
                PhraseChunker(
                    tags=[
                        Tag('FRW-NEG', phrase=RegexPhrase(r'\b(not)\b')),
                    ],
                    apply_iob2 = False,
                ),
                order=3
            ),
            TokenTaggerPipe(
                'neg_scope',
                focus='neg',
                tagger=Scoper(
                    scopes=[
                        Scope(
                            applied_tag='FRW-NEG',
                            scope_direction=ScopeDirection.RIGHT,
                            order=1,
                        )
                    ],
                ),
                order=4,
            )
        ]
    )

    context = Context(
        'We are not going to New York.',
        ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']
    )
    context = pipeline.execute(context)

    assert len(context.keys) == 8
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
    assert context.get('spacings') == [
      'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no'
    ]
    assert context.get('start_positions') == [
      '0', '3', '7', '11', '17', '20', '24', '28'
    ]
    assert context.get('end_positions') == [
      '1', '5', '9', '15', '18', '22', '27', '28'
    ]
    assert context.get('regex_ner') == ['', '', '', '', '', 'B-LOC', 'I-LOC', '']
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

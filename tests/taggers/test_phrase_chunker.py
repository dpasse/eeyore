import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.taggers import PhraseChunker
from eeyore.models import Tag, RegexPhrase, Context

def test_chunker_single_term_phrase():
    chunker = PhraseChunker(
        tags=[
            Tag('NEG', phrase=RegexPhrase(r'\b(not)\b')),
        ],
        apply_iob2=False
    )

    phrases = chunker.tag_text('We are not going to New York.')
    assert phrases == ['', '', 'NEG', '', '', '', '', '']

def test_chunker_when_multiple_terms_in_phrase():
    chunker = PhraseChunker(tags=[
        Tag('LOC', phrase=RegexPhrase(r'\b(New York)\b')),
    ])

    context = Context(
        'We went to New York.',
        ['We', 'went', 'to', 'New', 'York', '.']
    )
    phrases = chunker.tag(context)
    assert phrases == ['', '', '', 'B-LOC', 'I-LOC', '']

def test_chunker_with_two_different_phrases():
    chunker = PhraseChunker(tags=[
        Tag('NEG', phrase=RegexPhrase(r'\b(not)\b')),
        Tag('LOC', phrase=RegexPhrase(r'\b(New York)\b')),
    ])

    phrases = chunker.tag_text('We are not going to New York.')
    assert phrases == ['', '', 'B-NEG', '', '', 'B-LOC', 'I-LOC', '']

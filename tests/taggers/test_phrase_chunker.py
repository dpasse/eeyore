import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.taggers import PhraseChunker
from eeyore.models import Tag, RegexPhrase

def test_chuker_single_term_phrase():
    chunker = PhraseChunker(tags=[
        Tag('NEG', phrase=RegexPhrase(r'\b(not)\b')),
    ])

    tokens, phrases = chunker.tag('We are not going to New York.')

    assert tokens == ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']
    assert phrases == ['', '', 'NEG', '', '', '', '', '']

def test_PhraseChunker_when_multiple_terms_in_phrase():
    chunker = PhraseChunker(tags=[
        Tag('R', phrase=RegexPhrase(r'\b(New York)\b')),
    ])

    tokens, phrases = chunker.tag('We went to New York.')

    assert tokens == ['We', 'went', 'to', 'New', 'York', '.']
    assert phrases == ['', '', '', 'R', 'R', '']

def test_PhraseChunker_with_two_different_phrases():
    chunker = PhraseChunker(tags=[
        Tag('NEG', phrase=RegexPhrase(r'\b(not)\b')),
        Tag('R', phrase=RegexPhrase(r'\b(New York)\b')),
    ])

    tokens, phrases = chunker.tag('We are not going to New York.')

    assert tokens == ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']
    assert phrases == ['', '', 'NEG', '', '', 'R', 'R', '']

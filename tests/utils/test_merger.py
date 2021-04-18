import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.utils import Merger

def test_combine_tag_lists():
    tokens = ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']
    phrases = ['', '', 'NEG', '', '', 'LOC', 'LOC', '']

    combination = Merger.combine_tag_lists(tokens, phrases, separator='@')

    assert combination == [ 'We', 'are', 'not@NEG', 'going', 'to', 'New@LOC', 'York@LOC', '.']

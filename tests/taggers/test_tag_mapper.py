import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.taggers import TagMapper

def test_mapping_and_clear_if_no_map_found():
    pos = [
        'DT',
        'JJ',
        'NN',
        'VBD',
        'RB',
        'RB',
        'VBN',
        'CC',
        'VBZ',
        'RB',
        'NN',
        '.'
    ]

    tense_mappings = {
        'VBD': 'past',
        'VBG': 'present',
        'VBN': 'past',
        'VBP': 'present',
        'VBZ': 'present'
    }

    tag_mapper = TagMapper(
        tense_mappings,
        clear_if_missing=True
    )
    tags = tag_mapper.tag(pos)

    assert tags == [
        '',
        '',
        '',
        'past',
        '',
        '',
        'past',
        '',
        'present',
        '',
        '',
        ''
    ]

def test_mapping():
    tokens = ['negtaive', 'fales']
    spelling_mappings = {
      'negtaive': 'negative',
      'fales': 'false'
    }

    tag_mapper = TagMapper(spelling_mappings)
    tags = tag_mapper.tag(tokens)

    assert tags == [
        'negative',
        'false'
    ]

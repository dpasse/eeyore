import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.utils import iob2

def test_is_iob_tag_should_flag_iob_format_as_true():
    assert iob2.is_iob_tag('B-LOC')
    assert not iob2.is_iob_tag('LOC')

def test_clean_tag_should_clean():
    assert iob2.clean_tag('B-LOC') == 'LOC'
    assert iob2.clean_tag('LOC') == 'LOC'

def test_is_tag_connected_should_return_true_for_connected():
    assert iob2.is_tag_connected('I-LOC', 'B-LOC')
    assert iob2.is_tag_connected('I-LOC', 'I-LOC')
    assert iob2.is_tag_connected('LOC', 'LOC')

def test_is_tag_connected_should_return_false_for_not_connected():
    assert not iob2.is_tag_connected('B-LOC', 'B-LOC')
    assert not iob2.is_tag_connected('B-LOC', 'I-LOC')

def test_to_iob_tags_to_iob():
    tokens = ['NEG', 'NEG', 'NEG', '', 'NEG', 'NEG']
    converted_tokens = iob2.to_iob(tokens)
    assert converted_tokens == [
        'B-NEG',
        'I-NEG',
        'I-NEG',
        '',
        'B-NEG',
        'I-NEG'
    ]

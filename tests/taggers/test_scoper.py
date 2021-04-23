import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.taggers import Scoper
from eeyore.models import Scope, ScopeDirection

def test_forward_scope_should_move_right():
    scopes = [
        Scope(
            'NEG',
            scope_direction=ScopeDirection.RIGHT,
            order=1
        )
    ]
    scoper = Scoper(scopes)

    tokens = ['', '', 'NEG', '', '', '', '', '']

    scope_tags = scoper.tag(tokens)
    assert scope_tags == ['', '', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG']

def test_backward_scope_should_move_left():
    scopes = [
        Scope(
            'NEG',
            scope_direction=ScopeDirection.LEFT,
            order=1
        )
    ]
    scoper = Scoper(scopes)

    tokens = ['', '', 'NEG', '', '', '', '', '']

    scope_tags = scoper.tag(tokens)
    assert scope_tags == ['NEG', 'NEG', 'NEG', '', '', '', '', '']

def test_forward_scope_should_move_both_directions():
    scopes = [
        Scope(
            'NEG',
            scope_direction=ScopeDirection.TWOWAY,
            order=1
        ),
    ]
    scoper = Scoper(scopes)

    tokens = ['', '', 'NEG', '', '', '', '', '']

    scope_tags = scoper.tag(tokens)
    assert scope_tags == ['NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG', 'NEG']

def test_forward_scope_should_stop():
    scopes = [
        Scope(
            'NEG',
            scope_direction=ScopeDirection.RIGHT,
            order=1,
            stop_when=['TRANS']
        )
    ]
    scoper = Scoper(scopes)

    tokens = ['', '', 'NEG', '', '', '', 'TRANS', '']

    scope_tags = scoper.tag(tokens)
    assert scope_tags == ['', '', 'NEG', 'NEG', 'NEG', 'NEG', '', '']

def test_backward_scope_should_stop():
    scopes = [
        Scope(
            'NEG',
            scope_direction=ScopeDirection.LEFT,
            order=1,
            stop_when=['TRANS']
        )
    ]
    scoper = Scoper(scopes)

    tokens = ['TRANS', 'PHRASE', 'NEG', '', '', '', '', '']

    scope_tags = scoper.tag(tokens)
    assert scope_tags == ['', 'NEG', 'NEG', '', '', '', '', '']

def test_should_exit_after_max_travel_distance_hit():
    scopes = [
        Scope(
            'NEG',
            scope_direction=ScopeDirection.LEFT,
            order=1,
            stop_when=['TRANS'],
            max_travel_distance=2
        )
    ]
    scoper = Scoper(scopes)

    tokens = ['TRANS', 'PHRASE', '', '', '', '', 'NEG', '']

    scope_tags = scoper.tag(tokens)
    assert scope_tags == ['', '', '', '', 'NEG', 'NEG', 'NEG', '']

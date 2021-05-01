import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.rulesets import load_tags, load_scopes
from eeyore_nlp.rulesets.collection import available_tag_keys, available_scope_keys

def test_load_tags():
    tags = list(load_tags(available_tag_keys))
    assert len(tags) == 5

def test_load_scopes():
    scopes = list(load_scopes(available_scope_keys))
    assert len(scopes) == 1

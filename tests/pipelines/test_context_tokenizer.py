import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.pipelines import ContextTokenizer

def test_context_tokenizer():
    text = 'Jack lives in New York. Bob lives in San Francisco.'

    tokenizer = ContextTokenizer()
    contexts = list(tokenizer.execute(text))

    assert len(contexts) == 2
    assert contexts[0].get('tokens') == ['Jack', 'lives', 'in', 'New', 'York', '.']
    assert contexts[1].get('tokens') == ['Bob', 'lives', 'in', 'San', 'Francisco', '.']

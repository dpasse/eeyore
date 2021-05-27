import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.pipelines import ContextTokenizer, BlockContextTokenizer

def test_context_tokenizer():
    text = 'Jack lives in New York. Bob lives in San Francisco.'

    tokenizer = ContextTokenizer()
    contexts = list(tokenizer.execute(text))

    assert len(contexts) == 2
    assert contexts[0].get('tokens') == ['Jack', 'lives', 'in', 'New', 'York', '.']
    assert contexts[1].get('tokens') == ['Bob', 'lives', 'in', 'San', 'Francisco', '.']

def test_block_context_tokenizer():
    text = """
Jack: How are you today?
Bob: Great, thanks. How are you?
Jack: Ok...
    """

    tokenizer = BlockContextTokenizer(
        block_expressions=[
            '^(Jack|Bob):'
        ]
    )

    contexts = list(tokenizer.execute(text))

    assert len(contexts) == 4
    assert contexts[0].get('tokens') == ['How', 'are', 'you', 'today', '?']
    assert contexts[0].cache['header'] == 'Jack:'

    assert contexts[1].get('tokens') == ['Great', ',', 'thanks', '.']
    assert contexts[1].cache['header'] == 'Bob:'
    assert contexts[2].get('tokens') == ['How', 'are', 'you', '?']
    assert contexts[2].cache['header'] == 'Bob:'

    assert contexts[3].get('tokens') == ['Ok', '...']
    assert contexts[3].cache['header'] == 'Jack:'

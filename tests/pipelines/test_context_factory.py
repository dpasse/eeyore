import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.pipelines import ContextFactory, \
                                 TextPipeline, \
                                 ContractionsTextPipe, \
                                 PreTaggedContextFactory

def test_context_factory():
    pipeline = TextPipeline(
        pipes=[
            ContractionsTextPipe()
        ]
    )
    factory = ContextFactory(pipeline)
    context = factory.execute('We aren\'t going to New York.')

    assert context.get('tokens') == ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']

def test_context_factory():
    factory = PreTaggedContextFactory('negative-scope')

    sentence = '<NEG>Not going to the park</NEG>.'
    context = factory.execute(sentence, id=1)
    assert context.cache['id'] == 1
    assert context.get('negative-scope') == [
        'B-NEG',
        'I-NEG',
        'I-NEG',
        'I-NEG',
        'I-NEG',
        ''
    ]

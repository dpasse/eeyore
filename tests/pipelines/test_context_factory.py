import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.pipelines import ContextFactory, \
                             TextPipeline, \
                             ContractionsTextPipe

def test_context_factory():
    pipeline = TextPipeline(
        pipes=[
            ContractionsTextPipe()
        ]
    )
    factory = ContextFactory(pipeline)
    context = factory.execute('We aren\'t going to New York.')

    assert context.get('tokens') == ['We', 'are', 'not', 'going', 'to', 'New', 'York', '.']

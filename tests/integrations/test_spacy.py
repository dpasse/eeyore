import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.models.context import Context
from eeyore_nlp.integrations import SpacyIntegration

def test_integration():

    integration = SpacyIntegration('en_core_web_sm')
    doc = integration.loads(
      Context(
        'I am hungry!',
        ['I', 'am', 'hungry', '!']
      )
    )

    print(doc)

    #context = integration.from(doc)

    #assert context.get('tokens') == ['I', 'am', 'hungry', '!']

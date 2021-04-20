import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore.generators import MarkovChain
from eeyore.models import Relationship, RelationshipContainer

def test_markov_chain_generation():
    ## Possible outcomes:
    ## I am tired
    ## I am not tired
    ## I am very tired
    ## I am not very tired

    relationship_container = RelationshipContainer([
        Relationship('<start>', ['I']),
        Relationship('I', ['am']),
        Relationship('am', ['not', 'very', 'tired']),
        Relationship('not', ['very', 'tired']),
        Relationship('very', ['tired']),
        Relationship('tired', ['<end>']),
        Relationship('<end>', []),
    ])

    generated_sentence_chain = MarkovChain(seed=42).generate(relationship_container)
    sentence = [
        relationship.primary
        for relationship in generated_sentence_chain
    ]
    assert sentence == [
        '<start>',
        'I',
        'am',
        'tired',
        '<end>'
    ]

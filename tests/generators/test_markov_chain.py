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

    relationship_container = RelationshipContainer()
    relationship_container.add_many([
        Relationship('<start>', ['I']),
        Relationship('I', ['am']),
        Relationship('am', ['not']),  # compress to ['not', 'very', 'tired']
        Relationship('am', ['very']),
        Relationship('am', ['tired']),
        Relationship('not', ['very']),
        Relationship('not', ['tired']),
        Relationship('very', ['tired']),
        Relationship('tired', ['<end>']),
        Relationship('<end>', []),
    ])

    generated_sentence_chain = MarkovChain(seed=56).generate(relationship_container)
    sentence = [
        relationship.primary
        for relationship in generated_sentence_chain
    ]
    assert relationship_container['am'].children == ['not', 'very', 'tired']
    assert relationship_container['not'].children == ['very', 'tired']
    assert sentence == [
        '<start>',
        'I',
        'am',
        'very',
        'tired',
        '<end>'
    ]

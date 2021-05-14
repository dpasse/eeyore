import os
import sys

sys.path.insert(0, os.path.abspath('src'))

from eeyore_nlp.generators import MarkovChain
from eeyore_nlp.models import Relationship, RelationshipContainer, RelationshipKey

def test_markov_chain_generation():
    ## Possible outcomes:
    ## I am tired
    ## I am not tired
    ## I am very tired
    ## I am not very tired

    relationship_container = RelationshipContainer()
    relationship_container.add_many([
        Relationship(
            RelationshipKey('<start>'),
            [RelationshipKey('I')]
        ),
        Relationship(
            RelationshipKey('I'),
            [RelationshipKey('am')]
        ),
        Relationship(
            RelationshipKey('am'),
            [RelationshipKey('not')]
        ),  # compress to ['not', 'very', 'tired']
        Relationship(
            RelationshipKey('am'),
            [RelationshipKey('very')]
        ),
        Relationship(
            RelationshipKey('am'),
            [RelationshipKey('tired')]
        ),
        Relationship(
            RelationshipKey('not'),
            [RelationshipKey('very')]
        ),
        Relationship(
            RelationshipKey('not'),
            [RelationshipKey('tired')]
        ),
        Relationship(
            RelationshipKey('very'),
            [RelationshipKey('tired')]
        ),
        Relationship(
            RelationshipKey('tired'),
            [RelationshipKey('<end>')]
        ),
        Relationship(
            RelationshipKey('<end>'),
            []
        ),
    ])

    generated_sentence_chain = MarkovChain(seed=56).generate(relationship_container)
    sentence = [
        relationship.primary.term
        for relationship in generated_sentence_chain
    ]
    assert relationship_container['am'].children == [
        RelationshipKey('not'),
        RelationshipKey('very'),
        RelationshipKey('tired')
    ]
    assert relationship_container[RelationshipKey('not')].children == [
        RelationshipKey('very'),
        RelationshipKey('tired')
    ]
    assert sentence == [
        '<start>',
        'I',
        'am',
        'very',
        'tired',
        '<end>'
    ]

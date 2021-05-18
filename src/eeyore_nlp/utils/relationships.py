from typing import List
from ..models import Relationship, RelationshipKey, Context


class RelationshipBuilder():
    def __init__(self,
                 start_token: str = '<start>',
                 end_token: str = '<end>'):
        self.__start_token = start_token
        self.__end_token = end_token

    def create_neighbor_relationships(self,
                                      tokens: List[str]) -> List[Relationship]:
        tokens_start = [self.__start_token]
        tokens_start.extend(tokens)

        tokens_end = tokens[:]
        tokens_end.append(self.__end_token)

        generator = (
            (
                RelationshipKey(primary),
                RelationshipKey(secondary)
            )
            for primary, secondary
            in zip(tokens_start, tokens_end)
        )

        relationships: List[Relationship] = []
        for primary, secondary in generator:
            relationships.append(
                Relationship(
                    primary,
                    [secondary]
                )
            )

        relationships.append(
            Relationship(
                RelationshipKey(self.__end_token),
                []
            )
        )

        return relationships

    def create_relationships_by_context(
        self,
        attributes: List[str],
        context: Context
    ) -> List[Relationship]:
        # make tokens be the last attribute
        attributes.remove('tokens')
        attributes.append('tokens')

        tokens = context.get('tokens')
        attribute_lookup = {
            attribute: context.get(attribute)
            for attribute in attributes
        }

        tokens_start = [RelationshipKey(self.__start_token)]
        tokens_end = []

        for i in range(len(context)):
            key = RelationshipKey(
                tokens[i],
                [
                    attribute_lookup[attribute][i]
                    for attribute in attributes
                ]
            )

            tokens_start.append(key)
            tokens_end.append(key)

        tokens_end.append(
            RelationshipKey(self.__end_token)
        )

        generator = (
            (primary, secondary)
            for primary, secondary
            in zip(tokens_start, tokens_end)
        )

        relationships: List[Relationship] = []
        for primary, secondary in generator:
            relationships.append(
                Relationship(primary, [secondary])
            )

        relationships.append(
            Relationship(
                RelationshipKey(self.__end_token),
                []
            )
        )

        return relationships

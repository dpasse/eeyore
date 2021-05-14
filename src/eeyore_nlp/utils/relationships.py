from typing import List
from ..models import Relationship, RelationshipKey


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

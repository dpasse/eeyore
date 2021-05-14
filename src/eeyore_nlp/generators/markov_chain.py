from typing import List, Optional
import numpy as np
from ..models import Relationship, RelationshipContainer, RelationshipKey


class MarkovChain():
    def __init__(self,
                 start_state: str = '<start>',
                 end_state: str = '<end>',
                 seed: Optional[int] = None):
        self.__start_state = RelationshipKey(start_state)
        self.__end_state = RelationshipKey(end_state)

        if seed is not None:
            np.random.seed(seed)

    def generate(self,
                 relationships: RelationshipContainer,
                 kill: int = -1) -> List[Relationship]:
        relationship_collection: List[Relationship] = []

        if self.__start_state not in relationships:
            raise KeyError(
                'No start state exists in your relationship container.'
            )

        current_state = self.__start_state

        i = 1
        while current_state != self.__end_state:
            state: Relationship = relationships[current_state]
            relationship_collection.append(state)

            if kill != -1 and i >= kill:
                break

            # pull next state
            current_state = self._query(state)

            i += 1

        if current_state == self.__end_state:
            relationship_collection.append(
                relationships[current_state]
            )

        return relationship_collection

    @staticmethod
    def _query(relationship: Relationship) -> RelationshipKey:
        choices = relationship.children
        if len(choices) == 1:
            return choices[0]

        return np.random.choice(choices, size=1)[0]

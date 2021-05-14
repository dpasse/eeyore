from typing import Any, Dict, List, Optional


class RelationshipKey():
    def __init__(self,
                 term: str,
                 keys: Optional[List[str]] = None):
        self.__term = term

        if keys is None:
            keys = []

        if len(keys) == 0:
            self.__keys = [term]
        else:
            self.__keys = keys

    @property
    def term(self) -> str:
        return self.__term

    @property
    def keys(self) -> List[str]:
        return self.__keys

    def __hash__(self) -> int:
        return hash(','.join(self.__keys))

    def __eq__(self, o: object) -> bool:
        return o.__hash__() == self.__hash__()

    def __repr__(self) -> str:
        keys = ', '.join(
            [f'"{key}"' for key in self.keys]
        )
        return f'<"{self.term}", [{keys}]>'


class Relationship():
    def __init__(self,
                 item1: RelationshipKey,
                 item2: List[RelationshipKey],
                 attributes: Optional[Dict[str, Any]] = None):
        self.__item1 = item1
        self.__item2 = item2
        self.__attributes = attributes \
            if attributes is not None else {}

    @property
    def primary(self) -> RelationshipKey:
        return self.__item1

    @property
    def children(self) -> List[RelationshipKey]:
        return self.__item2

    @property
    def attributes(self) -> Optional[Dict[str, Any]]:
        return self.__attributes

    def __add__(self, obj):
        if self.primary != obj.primary:
            raise ValueError(
                'obj has a different "primary", both are not compatible.'
            )

        self.children.extend(obj.children)
        return self


class RelationshipContainer(dict):
    def __init__(self, relationships: Optional[List[Relationship]] = None):
        super().__init__()

        if relationships is not None:
            self.add_many(relationships)

    def add(self, relationship: Relationship):
        key = relationship.primary
        if key not in self:
            self[key] = relationship
        else:
            self[key] += relationship

    def add_many(self, relationships: List[Relationship]):
        for relationship in relationships:
            self.add(relationship)

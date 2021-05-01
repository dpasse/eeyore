from typing import Any, Dict, List, Optional


class Relationship():
    def __init__(self,
                 item1: str,
                 item2: List[str],
                 attributes: Optional[Dict[str, Any]] = None):
        self.__item1 = item1
        self.__item2 = item2
        self.__attributes = attributes \
            if attributes is not None else {}

    @property
    def primary(self) -> str:
        return self.__item1

    @property
    def children(self) -> List[str]:
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
            self[relationship.primary] = relationship
        else:
            self[key] += relationship

    def add_many(self, relationships: List[Relationship]):
        for relationship in relationships:
            self.add(relationship)

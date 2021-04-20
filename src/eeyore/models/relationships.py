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


class RelationshipContainer(dict):
    def __init__(self, relationships: Optional[List[Relationship]] = None):
        super().__init__()

        if relationships is not None:
            self.add_many(relationships)

    def add(self, relationship: Relationship):
        self[relationship.primary] = relationship

    def add_many(self, relationships: List[Relationship]):
        for relationship in relationships:
            self.add(relationship)

from typing import Any, Dict, Optional, TypeVar


T1 = TypeVar('T1')
T2 = TypeVar('T2')

class Relationship():
    def __init__(self,
                 item1: T1,
                 item2: T2,
                 attributes: Optional[Dict[str, Any]]):
        self.__item1 = item1
        self.__item2 = item2
        self.__attributes = attributes

    @property
    def primary(self) -> T1:
        return self.__item1

    @property
    def secondary(self) -> T2:
        return self.__item2

    @property
    def attributes(self) -> Optional[Dict[str, Any]]:
        return self.__attributes

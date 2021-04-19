from typing import Any, Dict, Optional


class Relationship():
    def __init__(self,
                 item1: Any,
                 item2: Any,
                 attributes: Optional[Dict[str, Any]]):
        self.__item1 = item1
        self.__item2 = item2
        self.__attributes = attributes

    @property
    def primary(self) -> Any:
        return self.__item1

    @property
    def secondary(self) -> Any:
        return self.__item2

    @property
    def attributes(self) -> Any:
        return self.__attributes

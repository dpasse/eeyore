from typing import Optional
from .phrases import RegexPhrase


class Tag():
    def __init__(self,
                 identifer: str,
                 phrase: RegexPhrase,
                 descending_order: Optional[int] = None):
        self.__identifer = identifer
        self.__phrase = phrase
        self.__order = descending_order \
            if descending_order is not None \
            else len(self.__phrase)

    @property
    def identifer(self) -> str:
        return self.__identifer

    @property
    def phrase(self) -> RegexPhrase:
        return self.__phrase

    @property
    def order(self) -> int:
        return self.__order

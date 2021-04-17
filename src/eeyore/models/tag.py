from .phrases import RegexPhrase


class Tag():
    def __init__(self, identifer: str, phrase: RegexPhrase):
        self.__identifer = identifer
        self.__phrase = phrase

    @property
    def identifer(self) -> str:
        return self.__identifer

    @property
    def phrase(self) -> RegexPhrase:
        return self.__phrase

    @property
    def order(self) -> int:
        return len(self.__phrase)

import re
from typing import List


class RegexPhrase():
    def __init__(self, phrase: str, flags: re.RegexFlag = None):
        self.__phrase = phrase
        self.__expression = \
            re.compile(self.__phrase) if flags is None \
            else re.compile(self.__phrase, flags=flags)

    @property
    def expression(self) -> re.Pattern:
        return self.__expression

    def find_all(self, text: str) -> List[str]:
        return self.__expression.findall(text)

    def sub(self, text: str, replacement: str) -> str:
        return self.__expression.sub(replacement, text)

    def __len__(self) -> int:
        return len(self.__phrase)

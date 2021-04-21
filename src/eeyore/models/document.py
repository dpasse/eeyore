from typing import Generator
from nltk.tokenize import sent_tokenize
from .context import Context


class Document():
    def __init__(self, text: str):
        self.__text = text

    @property
    def text(self) -> str:
        return self.__text

    @property
    def sentences(self) -> Generator[Context, None, None]:
        return (
            Context(sentence)
            for sentence in sent_tokenize(self.__text)
        )

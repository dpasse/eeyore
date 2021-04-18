from abc import ABC, abstractmethod

from ..taggers import Chunker, Scoper
from ..models import Context


class Pipe(ABC):
    def __init__(self, order: int):
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order

    @abstractmethod
    def execute(self, context: Context) -> Context:
        raise NotImplementedError()

class ChunkerPipe(Pipe):
    def __init__(self, key: str, chunker: Chunker, order: int):
        self.__key = key
        self.__chunker = chunker

        super().__init__(order)

    def execute(self, context: Context) -> Context:
        _, tags = self.__chunker.tag(context.sentence)
        context.add(
            self.__key,
            tags,
        )

        return context

class ScoperPipe(Pipe):
    def __init__(self, key: str, focus: str, scoper: Scoper, order: int):
        self.__key = key
        self.__focus = focus
        self.__scoper = scoper

        super().__init__(order)

    def execute(self, context: Context) -> Context:
        context.add(
            self.__key,
            self.__scoper.tag(context.get(self.__focus))
        )

        return context

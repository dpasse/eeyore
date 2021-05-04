from abc import ABC, abstractmethod
from typing import Generator
from ..models import Context


class AbsPipe(ABC):
    def __init__(self, order: int):
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order


class Tokenizer(ABC):
    @abstractmethod
    def execute(self, text: str) -> Generator[Context, None, None]:
        pass


class TextPipe(AbsPipe):
    @abstractmethod
    def execute(self, text: str) -> str:
        raise NotImplementedError()


class ContextPipe(AbsPipe):
    @abstractmethod
    def execute(self, context: Context) -> Context:
        raise NotImplementedError()

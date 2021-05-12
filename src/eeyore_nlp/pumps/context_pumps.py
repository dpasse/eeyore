from typing import Generator
from .abs import AbsTextPump
from ..pipelines import ContextTokenizer
from ..models import Context


class ContextPump():
    def __init__(self, pump: AbsTextPump, tokenizer: ContextTokenizer):
        self.__pump = pump
        self.__tokenizer = tokenizer

    def execute(self) -> Generator[Context, None, None]:
        for document in self.__pump.execute():
            for context in self.__tokenizer.execute(document):
                yield context

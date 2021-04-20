
from typing import List
from .pipes import Pipe
from ..models import Context


class Pipeline():
    def __init__(self, pipes: List[Pipe]):
        self.__pipes = sorted(
            pipes,
            key=lambda pipe: pipe.order,
        )

    @property
    def pipes(self) -> List[Pipe]:
        return self.__pipes

    def execute(self, text: str) -> Context:
        context = Context(text)
        for pipe in self.__pipes:
            context = pipe.execute(context)

        return context

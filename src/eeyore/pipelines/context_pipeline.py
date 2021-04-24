from typing import List
from .context_pipes import ContextPipe
from ..models import Context


class ContextPipeline():
    def __init__(self, pipes: List[ContextPipe]):
        self.__pipes = sorted(
            pipes,
            key=lambda pipe: pipe.order,
        )

    @property
    def pipes(self) -> List[ContextPipe]:
        return self.__pipes

    def execute(self, context: Context) -> Context:
        for pipe in self.__pipes:
            context = pipe.execute(context)

        return context


from typing import List
from .text_pipes import TextPipe


class TextPipeline():
    def __init__(self, pipes: List[TextPipe]):
        self.__pipes = sorted(
            pipes,
            key=lambda pipe: pipe.order,
        )

    @property
    def pipes(self) -> List[TextPipe]:
        return self.__pipes

    def execute(self, text: str) -> str:
        for pipe in self.__pipes:
            text = pipe.execute(text)

        return text

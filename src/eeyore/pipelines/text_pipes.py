from abc import abstractmethod
from .abs_pipe import AbsPipe


class TextPipe(AbsPipe):
    @abstractmethod
    def execute(self, text: str) -> str:
        raise NotImplementedError()


class EmptyTextPipe(TextPipe):
    def __init__(self):
        super().__init__(1)

    def execute(self, text: str) -> str:
        return text

from abc import ABC, abstractmethod
from nltk.tag import pos_tag

from ..taggers import SentenceChunker, Scoper
from ..models import Context
from ..ml import ContextBaseModel


class Pipe(ABC):
    def __init__(self, order: int):
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order

    @abstractmethod
    def execute(self, context: Context) -> Context:
        raise NotImplementedError()


class SentenceChunkerPipe(Pipe):
    def __init__(self, key: str, chunker: SentenceChunker, order: int):
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


class AttributePipe(Pipe):
    def execute(self, context: Context) -> Context:
        tokens = context.get('tokens')
        context.add(
            'pos',
            [tag for _, tag in pos_tag(tokens)],
        )

        return context


class MachineLearningContextPipe(Pipe):
    def __init__(self, key: str, model: ContextBaseModel, order: int):
        self.__key = key
        self.__model = model

        super().__init__(order)

    @property
    def model(self) -> ContextBaseModel:
        return self.__model

    def execute(self, context: Context) -> Context:
        context.add(
            self.__key,
            self.__model.tag(context),
        )

        return context

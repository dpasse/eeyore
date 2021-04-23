from abc import ABC, abstractmethod
from nltk.tag import pos_tag

from ..taggers import ContextChunker, Scoper
from ..models import Context
from ..ml import ContextBaseModel


class ContextPipe(ABC):
    def __init__(self, order: int):
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order

    @abstractmethod
    def execute(self, context: Context) -> Context:
        raise NotImplementedError()


class ChunkerPipe(ContextPipe):
    def __init__(self, key: str, chunker: ContextChunker, order: int):
        self.__key = key
        self.__chunker = chunker

        super().__init__(order)

    def execute(self, context: Context) -> Context:
        tags = self.__chunker.tag(context)
        context.add(
            self.__key,
            tags,
        )

        return context


class ScoperPipe(ContextPipe):
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


class TokenAttributesPipe(ContextPipe):
    def execute(self, context: Context) -> Context:
        tokens = context.get('tokens')
        context.add(
            'pos',
            [tag for _, tag in pos_tag(tokens)],
        )

        return context


class MachineLearningContextPipe(ContextPipe):
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

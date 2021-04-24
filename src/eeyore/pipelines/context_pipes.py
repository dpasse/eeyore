from abc import abstractmethod
from nltk.tag import pos_tag
from ..taggers import ContextChunker, Scoper
from ..models import Context
from ..ml import ContextBaseModel
from .abs_pipe import AbsPipe


class ContextPipe(AbsPipe):
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


class EmptyContextPipe(ContextPipe):
    def __init__(self):
        super().__init__(1)

    def execute(self, context: Context) -> Context:
        return context

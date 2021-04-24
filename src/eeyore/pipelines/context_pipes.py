import re
from abc import abstractmethod
from typing import List
from nltk.tag import pos_tag
from ..taggers import ContextChunker, Scoper
from ..models import Context
from ..ml import ContextBaseModel
from .abs_pipe import AbsPipe
from ..utils import SpellChecker, Merger


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
    def __init__(self,
                 spell_checker: SpellChecker = SpellChecker()):
        self.__spell_checker = spell_checker
        super().__init__(-1000)

    def execute(self, context: Context) -> Context:
        tokens = context.get('tokens')
        spacings = self._get_spacing(
            context.sentence,
            tokens
        )

        was_updated, tokens = self.__spell_checker.evaluate(tokens)
        if was_updated:
            return self.execute(
                Context(
                    Merger.generate_sentence(
                        tokens,
                        spacings
                    ),
                    tokens,
                    **context.cache
                )
            )

        context.add(
            'pos',
            self._get_pos(tokens),
        )
        context.add('spacings', spacings)
        context.add(
            'start_positions',
            self._get_start_positions(
                tokens,
                spacings
            )
        )
        context.add(
            'end_positions',
            self._get_end_positions(
                tokens,
                spacings
            )
        )

        return context

    def _get_pos(self, tokens: List[str]) -> List[str]:
        return [tag for _, tag in pos_tag(tokens)]

    def _get_spacing(self, text: str, tokens: List[str]) -> List[str]:
        spacing = []
        for token in tokens:
            text = re.sub(f'^{re.escape(token)}', '', text)
            spacing.append(
                'yes' if text.startswith(' ') else 'no'
            )
            text = text.strip()

        return spacing

    def _get_start_positions(self,
                             tokens: List[str],
                             spacings: List[str]) -> List[str]:
        start_position = []
        start = 0
        for i, token in enumerate(tokens):
            start_position.append(str(start))

            start += len(token)
            if spacings[i] == 'yes':
                start += 1

        return start_position

    def _get_end_positions(self,
                           tokens: List[str],
                           spacings: List[str]) -> List[str]:
        end = len(tokens[0]) - 1
        end_position = [str(end)]
        for i in range(1, len(tokens)):
            if spacings[i-1] == 'yes':
                # move forward
                end += 1

            end += len(tokens[i])
            end_position.append(str(end))

        return end_position


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

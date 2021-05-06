import re
from typing import List
from nltk.tag import pos_tag
from ..taggers import ContextChunker, TokenTagger
from ..models import Context
from ..utils import SpellChecker, Merger
from .abs import ContextPipe


class ChunkerPipe(ContextPipe):
    def __init__(self, key: str, chunker: ContextChunker, order: int):
        super().__init__(order)

        self.__key = key
        self.__chunker = chunker

    def execute(self, context: Context) -> Context:
        tags = self.__chunker.tag(context)
        context.add(
            self.__key,
            tags,
        )

        return context


class TokenTaggerPipe(ContextPipe):
    def __init__(self, key: str, focus: str, tagger: TokenTagger, order: int):
        super().__init__(order)

        self.__key = key
        self.__focus = focus
        self.__tagger = tagger

    def execute(self, context: Context) -> Context:
        context.add(
            self.__key,
            self.__tagger.tag(context.get(self.__focus))
        )

        return context


class MergerPipe(ContextPipe):
    def __init__(self,
                 key: str,
                 primary: str,
                 secondary: str,
                 order: int):
        super().__init__(order)

        self.__key = key
        self.__primary = primary
        self.__secondary = secondary

    def execute(self, context: Context) -> Context:
        context.add(
            self.__key,
            Merger.take_first(
                context.get(self.__primary),
                context.get(self.__secondary),
            ),
        )

        return context


class TokenAttributesPipe(ContextPipe):
    def __init__(self,
                 spell_checker: SpellChecker = SpellChecker()):
        super().__init__(-1000)

        self.__spell_checker = spell_checker

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
            if token in ['``', "''"] and text.startswith('"'):
                # nltk: starting " -> ``, ending " -> ''
                token = '"'

            text = re.sub(f'^{re.escape(token)}', '', text)
            answer = 'yes' if text.startswith(' ') else 'no'
            spacing.append(answer)
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


class EmptyContextPipe(ContextPipe):
    def __init__(self):
        super().__init__(1)

    def execute(self, context: Context) -> Context:
        return context

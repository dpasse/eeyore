import re
from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Optional, Tuple
from nltk.tokenize import sent_tokenize
from .context_pipeline import ContextPipeline
from .context_factory import ContextFactory
from .text_pipeline import TextPipeline
from ..models import Context


class Tokenizer(ABC):
    @abstractmethod
    def execute(self, text: str) -> Generator[Context, None, None]:
        pass


class ContextTokenizer(Tokenizer):
    def __init__(self,
                 context_factory: ContextFactory = ContextFactory(),
                 text_preprocessor: Optional[TextPipeline] = None,
                 context_pipeline: Optional[ContextPipeline] = None):
        self.__context_factory = context_factory
        self.__text_preprocessor = text_preprocessor
        self.__context_pipeline = context_pipeline

    def execute(self, text: str) -> Generator[Context, None, None]:
        text = self._preprocess_text(text)
        return (
            self._create_context(sentence, cache)
            for sentence, cache in self._split_text(text)
        )

    def _preprocess_text(self, text: str) -> str:
        if self.__text_preprocessor is None:
            return text

        return self.__text_preprocessor.execute(text)

    def _create_context(self, text: str, cache: Dict[str, Any]) -> Context:
        context = self.__context_factory.execute(
            text,
            **cache
        )

        return self._execute_context_pipeline(context)

    def _execute_context_pipeline(self, context: Context) -> Context:
        if self.__context_pipeline is None:
            return context

        return self.__context_pipeline.execute(context)

    def _split_text(self, text) -> Generator[Tuple[str, dict], None, None]:
        text = re.sub(r'\s+', ' ', text)
        return (
            (sentence, {'i': i})
            for i, sentence in enumerate(sent_tokenize(text))
        )


class BlockContextTokenizer(ContextTokenizer):
    def __init__(self,
                 block_expressions: List[str],
                 context_factory: ContextFactory = ContextFactory(),
                 text_preprocessor: Optional[TextPipeline] = None,
                 context_pipeline: Optional[ContextPipeline] = None):
        super().__init__(
            context_factory,
            text_preprocessor,
            context_pipeline
        )

        self.__block_expression = '(' + '|'.join(block_expressions) + ')'

    def _split_text(self, text) -> Generator[Tuple[str, dict], None, None]:
        block_header_expression = f'{self.__block_expression}(.*)'
        for block_i, block in enumerate(self._split_blocks(text)):
            text, header = block, ''
            matches = re.findall(block_header_expression, text)
            if len(matches) > 0:
                match = matches[0]
                header, text = match[0], match[-1]

            for i, sentence in enumerate(sent_tokenize(text.strip())):
                yield sentence, {
                    'header': header.strip(),
                    'block_i': block_i,
                    'i': i
                }

    def _split_blocks(self, text: str) -> List[str]:
        block_indexes = [
            match.start(0)
            for match in re.finditer(
                self.__block_expression,
                text,
                flags=re.MULTILINE
            )
        ]

        starting_indexes = [0]
        starting_indexes.extend(block_indexes)

        ending_indexes = block_indexes.copy()
        ending_indexes.append(-1)

        return [
            re.sub(
                r'\s+',
                ' ',
                text[s:i] if i > -1 else text[s:]
            )
            for s, i
            in zip(starting_indexes, ending_indexes)
        ]

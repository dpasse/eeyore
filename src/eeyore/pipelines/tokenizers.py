from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, Optional, Tuple
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
        return (
            (sentence, {'i': i})
            for i, sentence in enumerate(sent_tokenize(text))
        )

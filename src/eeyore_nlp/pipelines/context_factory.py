import re
from typing import Any, Dict, Optional
import numpy as np
from nltk.tokenize import word_tokenize
from .text_pipeline import TextPipeline
from ..models import Context, Tag, RegexPhrase
from ..taggers import PhraseChunker


class ContextFactory():
    def __init__(self,
                 pipeline: Optional[TextPipeline] = None):
        self.__pipeline = pipeline

    def execute(self,
                text: str,
                **kwargs: Dict[str, Any]) -> Context:
        text = self._preprocess_text(text)
        return Context(
            text,
            word_tokenize(text),
            **kwargs
        )

    def _preprocess_text(self, text: str) -> str:
        if self.__pipeline is None:
            return text

        return self.__pipeline.execute(text)


class PreTaggedContextFactory(ContextFactory):
    def __init__(self,
                 key: str,
                 pipeline: Optional[TextPipeline] = None):
        super().__init__(pipeline)

        self.__key = key

    def execute(self,
                text: str,
                **kwargs: Dict[str, Any]) -> Context:
        chunker = self._get_chunker(text)

        context = super().execute(
            re.sub(r'<[^<>]+?>', '', text),
            **kwargs
        )

        context.add(
            self.__key,
            chunker.tag(context)
        )

        return context

    def _get_chunker(self, text: str) -> PhraseChunker:
        tags = []
        for annotation in np.unique(
            re.findall(r'<([^</>]+?)>', text)
        ):
            for expression in re.findall(
                f'<{annotation}>(.+?)</{annotation}>',
                text
            ):
                tags.append(Tag(
                    annotation,
                    RegexPhrase('(' + re.escape(expression) + ')'),
                ))

        return PhraseChunker(
            tags=tags,
            apply_iob2=True
        )

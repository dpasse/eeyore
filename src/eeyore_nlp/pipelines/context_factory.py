from typing import Any, Dict, Optional
from nltk.tokenize import word_tokenize
from .text_pipeline import TextPipeline
from ..models import Context


class ContextFactory():
    def __init__(self,
                 pipeline: Optional[TextPipeline] = None):
        self.__pipeline = pipeline

    def execute(self, text: str, **kwargs: Dict[str, Any]) -> Context:
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

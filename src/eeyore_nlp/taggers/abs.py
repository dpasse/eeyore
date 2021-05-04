from abc import ABC, abstractmethod
from typing import List
from ..models import Context


class TokenTagger(ABC):
    @abstractmethod
    def tag(self, tags: List[str]) -> List[str]:
        raise NotImplementedError()


class TextChunker(ABC):
    @abstractmethod
    def tag_text(self, text: str) -> List[str]:
        raise NotImplementedError()


class ContextChunker(ABC):
    @abstractmethod
    def tag(self, context: Context) -> List[str]:
        raise NotImplementedError()

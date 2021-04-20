import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import numpy as np
from nltk.tokenize import word_tokenize
from ..models import Tag, Context
from ..generators import Alias


class TextChunker(ABC):
    @abstractmethod
    def tag_text(self, text: str) -> List[str]:
        raise NotImplementedError()


class ContextChunker(ABC):
    @abstractmethod
    def tag(self, context: Context) -> List[str]:
        raise NotImplementedError()


class PhraseChunker(TextChunker, ContextChunker):
    def __init__(self, tags: List[Tag]):
        self.__tags = list(
            sorted(
                tags,
                key=lambda tag: tag.order,
                reverse=True
            )
        )
        self.__alias = Alias()

    @property
    def tags(self) -> List[Tag]:
        return self.__tags

    def tag(self, context: Context) -> List[str]:
        return self.tag_text(context.sentence)

    def tag_text(self, text: str) -> List[str]:
        alias_cache: Dict[str, Tuple[str, str]] = {}

        for tag in self.__tags:
            for match in np.unique(tag.phrase.find_all(text)):
                key = self.__alias.get_alias()
                alias_cache[key] = (tag.identifer, match)
                text = re.sub(r'(' + match + r')', key, text)

        phrases: List[str] = []

        keys = list(alias_cache.keys())
        for token in word_tokenize(text):
            term = self._find_term_in_text(token, keys)
            if term is not None:
                identifier, subset = alias_cache[term]
                new_tokens = word_tokenize(
                    token.replace(term, subset)
                )

                phrases.extend([identifier for _ in new_tokens])
            else:
                phrases.append('')

        return phrases

    @staticmethod
    def _find_term_in_text(text: str, terms: List[str]) -> Optional[str]:
        for term in terms:
            if term in text:
                return term

        return None

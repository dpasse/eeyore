import re
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import numpy as np
from nltk.tokenize import word_tokenize
from ..models import Tag
from ..generators import Alias


class TextChunker(ABC):
    @abstractmethod
    def tag(self, sentence: str) -> Tuple[List[str], List[str]]:
        raise NotImplementedError()


class PhraseChunker(TextChunker):
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

    def tag(self, sentence: str) -> Tuple[List[str], List[str]]:
        alias_cache: Dict[str, Tuple[str, str]] = {}

        for tag in self.__tags:
            for match in np.unique(tag.phrase.find_all(sentence)):
                key = self.__alias.get_alias()
                alias_cache[key] = (tag.identifer, match)
                sentence = re.sub(r'(' + match + r')', key, sentence)

        tokens: List[str] = []
        phrases: List[str] = []

        keys = list(alias_cache.keys())
        for token in word_tokenize(sentence):
            term = self._find_term_in_text(token, keys)
            if term is not None:
                identifier, subset = alias_cache[term]
                new_tokens = word_tokenize(
                    token.replace(term, subset)
                )

                tokens.extend(new_tokens)
                phrases.extend([identifier for _ in new_tokens])
            else:
                tokens.append(token)
                phrases.append('')

        return tokens, phrases

    @staticmethod
    def _find_term_in_text(text: str, terms: List[str]) -> Optional[str]:
        for term in terms:
            if term in text:
                return term

        return None

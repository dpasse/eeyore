import re
from typing import List, Tuple
import numpy as np
from nltk.tokenize import word_tokenize
from ..models import Tag
from ..generators import Alias


class Chunker():
    def __init__(self, tags: List[Tag]):
        self.__tags = list(sorted(tags, key=lambda tag: tag.order, reverse=True))
        self.__alias = Alias()

    @property
    def tags(self) -> List[Tag]:
        return self.__tags

    def tag(self, sentence: str) -> Tuple[List[str], List[str]]:
        alias_cache = {}

        for tag in self.__tags:
            for match in np.unique(tag.phrase.find_all(sentence)):
                key = self.__alias.get_alias()
                alias_cache[key] = (tag.identifer, word_tokenize(match))

                sentence = re.sub(r'(' + match + r')', key, sentence)

        tokens: List[str] = []
        phrases: List[str] = []

        for token in word_tokenize(sentence):
            if token in alias_cache:
                identifier, subset = alias_cache[token]

                tokens.extend(subset)
                phrases.extend([ identifier for _ in subset ])
            else:
                tokens.append(token)
                phrases.append('')

        return tokens, phrases

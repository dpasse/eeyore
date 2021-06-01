import re
from typing import Dict, List, Optional, Tuple
import numpy as np
import nltk
from nltk.chunk import RegexpParser
from nltk.tokenize import word_tokenize
from ..models import Tag, Context
from ..generators import Alias
from .abs import ContextChunker, TextChunker


class PhraseChunker(TextChunker, ContextChunker):
    def __init__(self, tags: List[Tag], apply_iob2: bool = True):
        self.__tags = list(
            sorted(
                tags,
                key=lambda tag: tag.order,
                reverse=True
            )
        )
        self.__apply_iob2 = apply_iob2
        self.__alias = Alias()

    @property
    def tags(self) -> List[Tag]:
        return self.__tags

    def tag(self, context: Context) -> List[str]:
        return self.tag_text(context.sentence)

    def tag_text(self, text: str) -> List[str]:
        alias_cache: Dict[str, Tuple[str, str]] = {}
        text = self._tag_text(text, alias_cache)

        keys = list(alias_cache.keys())
        phrases: List[str] = []
        for token in word_tokenize(text):
            term = self._find_term_in_text(token, keys)
            if term is not None:
                identifier, subset = alias_cache[term]
                new_tokens = word_tokenize(
                    token.replace(term, subset)
                )

                for i, _ in enumerate(new_tokens):
                    index = ''
                    if self.__apply_iob2:
                        index = 'B-' if i == 0 else 'I-'

                    phrase = f'{index}{identifier}'
                    phrases.append(phrase)

            else:
                phrases.append('')

        return phrases

    def _tag_text(self,
                  text: str,
                  alias_cache: Dict[str, Tuple[str, str]]) -> str:
        for tag in self.__tags:
            for match in np.unique(tag.phrase.find_all(text)):
                key = self.__alias.get_alias()
                alias_cache[key] = (tag.identifer, match)
                text = re.sub(
                    r'(\s|\b|^|\W)(' + match + r')(\s|\b|$|\W)',
                    r'\g<1>' + key + r'\g<3>',
                    text
                )

        return text

    @staticmethod
    def _find_term_in_text(text: str, terms: List[str]) -> Optional[str]:
        for term in terms:
            if term in text:
                return term

        return None


class TreeChunker(ContextChunker):
    def __init__(self,
                 patterns: str,
                 loop: int = 1,
                 trace: int = 0,
                 attribute: str = 'pos',
                 apply_iob2: bool = True) -> None:
        self.__attribute = attribute
        self.__regex_parser = RegexpParser(patterns,
                                           root_label='',
                                           loop=loop,
                                           trace=trace)
        self.__apply_iob2 = apply_iob2

    def tag(self, context: Context) -> List[str]:
        tokens_to_chunk = [
            'NULL' if tk == '' else tk
            for tk in context.get(self.__attribute)
        ]

        chunk_struct = list(
            zip(
                context.get('tokens'),
                tokens_to_chunk
            )
        )

        return self._traverse_tree(
            self.__regex_parser.parse(chunk_struct)
        )

    def _traverse_tree(self, tree, is_subtree: bool = False):
        tags = []
        for i, subtree in enumerate(tree):
            if isinstance(subtree, nltk.tree.Tree):
                tags.extend(
                    self._traverse_tree(subtree, True)
                )
            else:
                tag = tree.label()
                if is_subtree:
                    index = ''
                    if self.__apply_iob2:
                        index = 'B-' if i == 0 else 'I-'

                    tag = f'{index}{tag}'

                tags.append(tag)

        return tags

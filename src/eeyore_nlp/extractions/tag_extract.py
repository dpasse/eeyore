from typing import Dict, List, Tuple
from ..models import Context
from ..utils import iob2


class TagExtract():
    def __init__(self,
                 attribute: str,
                 valid_tags: List[str]) -> None:
        self.__attribute = attribute
        self.__valid_tags = valid_tags

    def evaluate(self, context: Context) -> dict:
        data = list(
          zip(
            context.get('tokens'),
            context.get(self.__attribute)
          )
        )

        tag = ''

        cache: List[Tuple[int, str]] = []
        extracts: Dict[str, List[List[Tuple[int, str]]]] = {
            tag: [] for tag in self.__valid_tags
        }

        for i, (token, attribute) in enumerate(data):
            if self._is_valid_tag(attribute):
                is_tag_connected = iob2.is_tag_connected(attribute, tag)
                if not is_tag_connected and len(cache) > 0:
                    key = iob2.clean_tag(tag)
                    extracts[key].append(cache.copy())
                    cache.clear()

                tag = attribute
                cache.append((i, token))

        if len(cache) > 0:
            key = iob2.clean_tag(tag)
            extracts[key].append(cache)

        return extracts

    def _is_valid_tag(self, tag) -> bool:
        return iob2.clean_tag(tag) in self.__valid_tags

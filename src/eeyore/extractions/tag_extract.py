from typing import Dict, List, Tuple
from ..models import Context


class TagExtract():
    def __init__(self,
                 attribute: str,
                 valid_tags: str) -> None:
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
            if attribute in self.__valid_tags:
                if tag != attribute and len(cache) > 0:
                    extracts[tag].append(cache)
                    cache.clear()

                tag = attribute
                cache.append((i, token))

        if len(cache) > 0:
            extracts[tag].append(cache)

        return extracts

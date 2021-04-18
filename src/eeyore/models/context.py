from typing import Dict, List


class Context():
    def __init__(self, text: str, tokens: List[str], **kwargs):
        self.__text = text
        self.__expected_length = len(tokens)
        self.__container: Dict[str, List[str]] = {
            'tokens': tokens
        }

        for key, value in kwargs.items():
            self.add(key, value)

    @property
    def sentence(self) -> str:
        return self.__text

    @property
    def keys(self) -> List[str]:
        return list(self.__container.keys())

    def get(self, key: str) -> List[str]:
        if not key in self.__container:
            raise KeyError(
                f'{key} not found.'
            )

        return self.__container[key]

    def add(self, key: str, tags: List[str]):
        if self.__expected_length != len(tags):
            raise ValueError(
                f'for key == {key}, ' +
                f'tags must have a length of {self.__expected_length}, ' +
                f'but was {len(tags)}.'
            )

        self.__container[key] = tags

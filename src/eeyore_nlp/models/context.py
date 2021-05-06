from typing import Any, Dict, List


class Context():
    def __init__(self, text: str, tokens: List[str], **kwargs: Dict[str, Any]):
        self.__text = text
        self.__expected_length = len(tokens)
        self.__container: Dict[str, List[str]] = {
            'tokens': tokens
        }

        self.__cache: Dict[str, Any] = kwargs

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return self.get(instance)

    @property
    def sentence(self) -> str:
        return self.__text

    @property
    def cache(self) -> Dict[str, Any]:
        return self.__cache

    @property
    def keys(self) -> List[str]:
        return list(self.__container.keys())

    def get(self, key: str) -> List[str]:
        if key not in self.__container:
            return ['' for _ in range(self.__len__())]

        return self.__container[key]

    def add(self,
            key: str,
            tags: List[str]):
        if self.__expected_length != len(tags):
            raise ValueError(
                f'for key == {key}, ' +
                f'tags must have a length of {self.__expected_length}, ' +
                f'but was {len(tags)}.'
            )

        if all(len(tag) == 0 for tag in tags):
            return

        self.__container[key] = tags

    def remove(self, key: str):
        if key not in self.__container:
            return

        self.__container.__delitem__(key)

    def __len__(self) -> int:
        return len(self.get('tokens'))

    def __hash__(self) -> int:
        return hash(self.__text)

from typing import Dict, List


class TagMapper():
    def __init__(self,
                 mappings: Dict[str, str],
                 clear_if_missing: bool = False):
        self.__mappings = mappings
        self.__clear_if_missing = clear_if_missing

    def tag(self, tags: List[str]) -> List[str]:
        return [
            self._map(tag)
            for tag
            in tags
        ]

    def _map(self, tag: str) -> str:
        for key in [tag, tag.lower()]:
            if key in self.__mappings:
                return self.__mappings[key]

        return '' if self.__clear_if_missing else tag

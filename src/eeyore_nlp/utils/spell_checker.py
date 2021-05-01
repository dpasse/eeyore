from typing import Dict, List, Optional, Tuple


class SpellChecker():
    def __init__(self,
                 dictionary: Optional[Dict[str, str]] = None):
        self.__dictionary = dictionary

    def evaluate(self, tokens: List[str]) -> Tuple[bool, List[str]]:
        token_list_was_updated = False
        if self.__dictionary is None:
            return token_list_was_updated, tokens

        collection = []
        for token in tokens:
            token_in_lowercase = token.lower()
            if token_in_lowercase in self.__dictionary:
                token = self.__dictionary[token_in_lowercase]
                token_list_was_updated = True

            collection.append(token)

        return token_list_was_updated, collection

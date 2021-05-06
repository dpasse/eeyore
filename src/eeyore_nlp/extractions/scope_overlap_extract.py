from typing import List
from ..models import Context
from ..utils import Merger


class ScopeOverlapExtract():
    __e1_attribute = 'e1'
    __e2_attribute = 'e2'
    __relationship_attribute = 'REL'

    def __init__(self,
                 e1: str,
                 e2: str):
        self.__e1 = e1
        self.__e2 = e2
        self.__attributes = [e1, e2]

    def evaluate(self, context: Context) -> List[str]:
        tokens = Merger.combine(
            context,
            self.__attributes
        )

        partial_scope = []
        relationship_scope = []
        for token in tokens:
            tag = self._get_attribute(
                self.__e1 in token.keys(),
                self.__e2 in token.keys()
            )

            if len(tag) != 0:
                partial_scope.append(tag)
                continue

            relationship_scope.extend(
                self._handle_partial_scope(partial_scope)
            )
            relationship_scope.append(tag)
            partial_scope.clear()

        if len(partial_scope) > 0:
            relationship_scope.extend(
                self._handle_partial_scope(partial_scope)
            )

        return relationship_scope

    def _get_attribute(self,
                       has_e1: bool,
                       has_e2: bool) -> str:
        if has_e1 and has_e2:
            return self.__relationship_attribute

        if has_e1:
            return self.__e1_attribute

        if has_e2:
            return self.__e2_attribute

        return ''

    def _handle_partial_scope(self,
                              scope: List[str]) -> List[str]:
        if len(scope) == 0:
            # no partial scope exists, return empty list
            return []

        if self.__relationship_attribute in scope:
            # relationship applies
            return [
                self.__relationship_attribute
                for _
                in scope
            ]

        # relationship does not apply, cancel out scope
        return [
            ''
            for _
            in scope
        ]

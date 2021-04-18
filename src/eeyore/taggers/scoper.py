from typing import List, Optional

from ..models import Scope, ScopeDirection
from ..utils import Merger


class Scoper():
    def __init__(self, scopes: List[Scope]):
        self.__rules = {
            ScopeDirection.FORWARD: sorted([
                scope
                for scope in scopes
                if scope.moves_forward
            ], key=lambda scope: scope.order),
            ScopeDirection.BACKWARD: sorted([
                scope
                for scope in scopes
                if scope.moves_backward
            ], key=lambda scope: scope.order),
        }

    def tag(self,
            tags: List[str],
            dominate_scope_direction: ScopeDirection = ScopeDirection.FORWARD) -> List[str]:
        forward_scope_tags = self._run_scopes(
            tags,
            scope_direction=ScopeDirection.FORWARD
        )

        backward_scope_tags = list(reversed(self._run_scopes(
            reversed(tags),
            scope_direction=ScopeDirection.BACKWARD
        )))

        if dominate_scope_direction == ScopeDirection.FORWARD:
            return Merger.take_first(
                forward_scope_tags,
                backward_scope_tags
            )

        return Merger.take_first(
            backward_scope_tags,
            forward_scope_tags
        )

    def _run_scopes(self, tags: List[str], scope_direction: ScopeDirection) -> List[str]:
        scope_tags = []

        current_scope = None
        scopes = self.__rules[scope_direction]
        for tag in tags:
            scope = self._find_first_scope(tag, scopes)
            if scope is not None:
                current_scope = scope

            need_to_cancel_scope = current_scope is not None \
                and current_scope.should_stop(tag)

            if need_to_cancel_scope:
                current_scope = None

            identifier = '' \
                if current_scope is None \
                else current_scope.applied_tag

            scope_tags.append(identifier)

        return scope_tags

    @staticmethod
    def _find_first_scope(tag: str, scopes: List[Scope]) -> Optional[Scope]:
        for scope in scopes:
            if tag == scope.applied_tag:
                return scope

        return None

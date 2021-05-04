from typing import Dict, List, Optional
from ..models import Scope, ScopeDirection
from ..utils import Merger
from .abs import TokenTagger


class Scoper(TokenTagger):
    def __init__(self,
                 scopes: List[Scope],
                 top_direction: ScopeDirection = ScopeDirection.RIGHT):
        self.__rules = {
            ScopeDirection.RIGHT: sorted([
                scope
                for scope in scopes
                if scope.moves_forward
            ], key=lambda scope: scope.order),
            ScopeDirection.LEFT: sorted([
                scope
                for scope in scopes
                if scope.moves_backward
            ], key=lambda scope: scope.order),
        }
        self.__top_direction = top_direction

    @property
    def rules(self) -> Dict[ScopeDirection, List[Scope]]:
        return self.__rules

    def tag(self,
            tags: List[str]) -> List[str]:
        forward_scope_tags = self._run_scopes(
            tags,
            scope_direction=ScopeDirection.RIGHT
        )

        backward_scope_tags = list(reversed(self._run_scopes(
            list(reversed(tags)),
            scope_direction=ScopeDirection.LEFT
        )))

        if self.__top_direction == ScopeDirection.RIGHT:
            return Merger.take_first(
                forward_scope_tags,
                backward_scope_tags
            )

        return Merger.take_first(
            backward_scope_tags,
            forward_scope_tags
        )

    def _run_scopes(self,
                    tags: List[str],
                    scope_direction: ScopeDirection) -> List[str]:
        scope_tags = []
        current_scope = None
        travel_distance = 0

        scopes = self.__rules[scope_direction]
        for tag in tags:
            scope = self._find_first_scope(tag, scopes)
            if scope is not None:
                current_scope = scope
                travel_distance = 0
            elif current_scope is not None:
                travel_distance += 1

            need_to_cancel_scope = current_scope is not None \
                and current_scope.should_stop(travel_distance, tag)

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

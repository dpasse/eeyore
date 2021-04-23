from typing import List, Optional
from enum import Enum


class ScopeDirection(Enum):
    RIGHT = 1
    LEFT = 2
    TWOWAY = 3


class Scope():
    def __init__(self,
                 applied_tag: str,
                 scope_direction: ScopeDirection,
                 order: int,
                 stop_when: Optional[List[str]] = None,
                 max_travel_distance: Optional[int] = None):
        self.__applied_tag = applied_tag
        self.__scope_direction = scope_direction
        self.__order = order
        self.__stop_when = stop_when
        self.__max_travel_distance = max_travel_distance

    @property
    def applied_tag(self) -> str:
        return self.__applied_tag

    @property
    def scope_direction(self) -> ScopeDirection:
        return self.__scope_direction

    @property
    def order(self) -> int:
        return self.__order

    @property
    def stop_when(self) -> List[str]:
        if self.__stop_when is None:
            return []

        return self.__stop_when

    @property
    def moves_forward(self) -> bool:
        return self.__scope_direction == ScopeDirection.RIGHT \
            or self.__scope_direction == ScopeDirection.TWOWAY

    @property
    def moves_backward(self) -> bool:
        return self.__scope_direction == ScopeDirection.LEFT \
            or self.__scope_direction == ScopeDirection.TWOWAY

    def should_stop(self, travel_distance: int, tag: str = '') -> bool:
        early_exit = travel_distance > self.__max_travel_distance \
            if self.__max_travel_distance is not None \
            else False

        return early_exit or \
            self.__stop_when is not None \
            and tag in self.__stop_when

from abc import ABC


class AbsPipe(ABC):
    def __init__(self, order: int):
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order

from abc import ABC, abstractmethod
from typing import Generator
from ..models import Context


class AbsTextPump(ABC):
    @abstractmethod
    def execute(self) -> Generator[str, None, None]:
        raise NotImplementedError()


class AbsContextPump(ABC):
    @abstractmethod
    def execute(self) -> Generator[Context, None, None]:
        raise NotImplementedError()

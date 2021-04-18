from typing import List
from abc import ABC, abstractmethod
from ..models import Context


class ContextModel(ABC):
    @abstractmethod
    def tag(self, context: Context) -> List[str]:
        raise NotImplementedError()

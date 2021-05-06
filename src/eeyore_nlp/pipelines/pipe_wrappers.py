from typing import List, Optional
from ..models import Context
from .abs import ContextPipe
from .context_pipeline import ContextPipeline


class ContextPipeWrapper(ContextPipe):
    def __init__(self,
                 pipes: List[ContextPipe],
                 order: int,
                 attributes_to_discard: Optional[List[str]] = None):
        super().__init__(order)

        self.__inner_pipeline = ContextPipeline(pipes)
        self.__attributes_to_discard = attributes_to_discard \
            if attributes_to_discard is not None \
            else []

    def execute(self, context: Context) -> Context:
        context = self.__inner_pipeline.execute(context)
        for attribute in self.__attributes_to_discard:
            context.remove(attribute)

        return context

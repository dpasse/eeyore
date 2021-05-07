import spacy
from spacy.tokens import Doc
from ..models import Context


class SpacyIntegration():
    def __init__(self, model_name: str):
        self.__spacy = spacy.load(model_name)

    @property
    def spacy(self):
        return self.__spacy

    def load(self, context: Context) -> Doc:
        doc = Doc(
            self.__spacy.vocab,
            words=context.get('tokens'),
            spaces=context.get('spacings')
        )

        for _, parsing_method in self.__spacy.pipeline:
            doc = parsing_method(doc)

        return doc

    def dump(self, doc: Doc) -> Context:
        return Context(
            doc.text,
            [token.text for token in doc],
        )

import re
from abc import abstractmethod
from .abs_pipe import AbsPipe


class TextPipe(AbsPipe):
    @abstractmethod
    def execute(self, text: str) -> str:
        raise NotImplementedError()


class EmptyTextPipe(TextPipe):
    def __init__(self):
        super().__init__(1)

    def execute(self, text: str) -> str:
        return text


class ContractionsTextPipe(TextPipe):
    def __init__(self):
        super().__init__(1)

    def execute(self, text: str) -> str:
        flags = re.IGNORECASE | re.MULTILINE
        text = re.sub(r'`', "'", text, flags=flags)

        # starts / ends with '
        text = re.sub(
            r"(\s|^)'(aight|cause)(\s|$)",
            r'\g<1>\g<2>\g<3>',
            text, flags=flags
        )

        text = re.sub(
            r"(\s|^)'t(was|is)(\s|$)", r'\g<1>it \g<2>\g<3>',
            text,
            flags=flags
        )

        text = re.sub(
            r"(\s|^)ol'(\s|$)",
            r'\g<1>old\g<2>',
            text, flags=flags
        )

        # expand words without '
        text = re.sub(r"\b(aight)\b", 'alright', text, flags=flags)
        text = re.sub(r'\b(cause)\b', 'because', text, flags=flags)
        text = re.sub(r'\b(finna|gonna)\b', 'going to', text, flags=flags)
        text = re.sub(r'\b(gimme)\b', 'give me', text, flags=flags)
        text = re.sub(r"\b(give'n)\b", 'given', text, flags=flags)
        text = re.sub(r"\b(howdy)\b", 'how do you do', text, flags=flags)
        text = re.sub(r"\b(gotta)\b", 'got to', text, flags=flags)
        text = re.sub(r"\b(innit)\b", 'is it not', text, flags=flags)
        text = re.sub(r"\b(can)(not)\b", r'\g<1> \g<2>', text, flags=flags)
        text = re.sub(r"\b(wanna)\b", 'want to', text, flags=flags)
        text = re.sub(r"\b(methinks)\b", 'me thinks', text, flags=flags)

        # one offs,
        text = re.sub(r"\b(o'er)\b", 'over', text, flags=flags)
        text = re.sub(r"\b(ne'er)\b", 'never', text, flags=flags)
        text = re.sub(r"\b(o'?clock)\b", 'of the clock', text, flags=flags)
        text = re.sub(r"\b(ma'am)\b", 'madam', text, flags=flags)
        text = re.sub(r"\b(giv'n)\b", 'given', text, flags=flags)
        text = re.sub(r"\b(e'er)\b", 'ever', text, flags=flags)
        text = re.sub(r"\b(d'ye)\b", 'do you', text, flags=flags)
        text = re.sub(r"\b(e'er)\b", 'ever', text, flags=flags)
        text = re.sub(r"\b(d'ye)\b", 'do you', text, flags=flags)
        text = re.sub(r"\b(g'?day)\b", 'good day', text, flags=flags)
        text = re.sub(r"\b(ain|amn)'?t\b", 'am not', text, flags=flags)
        text = re.sub(r"\b(are|can)'?t\b", r'\g<1> not', text, flags=flags)
        text = re.sub(r"\b(let)'?s\b", r'\g<1> us', text, flags=flags)

        # major expansions involving smaller,
        text = re.sub(
            r"\b(y'all'dn't've'd)\b",
            'you all would not have had',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(y'all're)\b",
            'you all are',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(y'all'd've)\b",
            'you all would have',
            text,
            flags=flags
        )
        text = re.sub(
            r"(\s)(y'all)(\s)",
            r'\g<1>you all\g<2>',
            text,
            flags=flags
        )

        # minor,
        text = re.sub(r"\b(won)'?t\b", 'will not', text, flags=flags)
        text = re.sub(r"\b(he'd)\b", 'he had', text, flags=flags)

        # major,
        text = re.sub(
            r"\b(I|we|who)'?d'?ve\b",
            r'\g<1> would have',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(could|would|must|should|would)n'?t'?ve\b",
            r'\g<1> not have',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(he)'?dn'?t'?ve'?d\b",
            r'\g<1> would not have had',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(daren|daresn|dasn)'?t",
            'dare not',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(he|how|i|it|she|that|there|these)'?ll\b",
            r'\g<1> will',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(they|we|what|where|which|who|you)'?ll\b",
            r'\g<1> will',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(everybody|everyone|he|how|it|she|somebody|someone)'?s\b",
            r'\g<1> is',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(something|thatthere|this|what|when|where|which|who|why)'?s\b",
            r'\g<1> is',
            text,
            flags=flags
        )
        text = re.sub(r"\b(I)'?m'a\b", r'\g<1> am about to', text, flags=flags)
        text = re.sub(r"\b(I)'?m'o\b", r'\g<1> am going to', text, flags=flags)
        text = re.sub(r"\b(I)'?m\b", r'\g<1> am', text, flags=flags)
        text = re.sub(r"\b(shan't)\b", 'shall not', text, flags=flags)
        text = re.sub(
            r"\b(are|could|did|does|do|go|had|has|have|is|may|might)n'?t\b",
            r'\g<1> not',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(need|ought|shall|should|was|were|would)n'?t\b",
            r'\g<1> not',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(could|had|he|i|may|might|must|should|these|they|those)'?ve\b",
            r'\g<1> have',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(to|we|what|where|which|who|would|you)'?ve\b",
            r'\g<1> have',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(how|so|that|there|these|they|those)'?re\b",
            r'\g<1> are',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(we|what|where|which|who|why|you)'?re\b",
            r'\g<1> are',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(I|it|she|that|there|they|we|which|you)'?d\b",
            r'\g<1> had',
            text,
            flags=flags
        )
        text = re.sub(
            r"\b(how|what|where|who|why)'?d\b",
            r'\g<1> did',
            text,
            flags=flags
        )

        return text

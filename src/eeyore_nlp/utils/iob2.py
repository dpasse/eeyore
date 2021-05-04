from typing import List
from ..models import Context


def is_iob_tag(tag: str) -> bool:
    return tag.startswith('B-') or tag.startswith('I-')


def clean_tag(tag: str) -> str:
    if is_iob_tag(tag):
        return tag[2:]

    return tag


def is_tag_connected(new_tag: str, previous_tag: str) -> bool:
    if previous_tag.startswith('B-') and new_tag.startswith('B-'):
        # B, B
        return False

    if previous_tag.startswith('I-') and new_tag.startswith('B-'):
        # I, B
        return False

    # either B, I or I, I
    return clean_tag(previous_tag) == clean_tag(new_tag)


def to_iob(tokens: List[str]) -> List[str]:
    previous_tag = ''
    converted_tokens = []
    for token in tokens:
        tag = token
        if token not in ['', 'O'] and not is_iob_tag(token):
            if clean_tag(previous_tag) == token:
                tag = f'I-{tag}'
            else:
                tag = f'B-{tag}'

        converted_tokens.append(tag)
        previous_tag = tag

    return converted_tokens


def to_xml(context: Context, attribute_key: str) -> str:
    p_tag = ''
    tokens: List[str] = []
    for token, tag in zip(
        context.get('tokens'),
        context.get(attribute_key)
    ):
        if p_tag not in (tag, ''):
            previous_token = tokens[-1]
            tokens[-1] = \
                f'{previous_token}</{p_tag}>'
            p_tag = ''

        if p_tag == '' and tag != '':
            tokens.append(
                f'<{tag}>{token}'
            )
        else:
            tokens.append(token)

        p_tag = tag

    if p_tag != '':
        previous_token = tokens[-1]
        tokens[-1] = \
            f'{previous_token}</{p_tag}>'

    sentence = ''
    for token, spacing in zip(
        tokens,
        context.get('spacings')
    ):
        sentence += token
        sentence += ' ' if spacing == 'yes' else ''

    return sentence

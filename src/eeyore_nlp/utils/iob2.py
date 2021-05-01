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

from typing import List
from ..models import Tag, RegexPhrase, Scope, ScopeDirection


def _map_regex_phrases(identifier: str,
                       regex_phrases: List[RegexPhrase]) -> List[Tag]:
    return [
        Tag(identifier, phrase=regex_phrase)
        for regex_phrase
        in regex_phrases
    ]


negative_tags = _map_regex_phrases('FRW-NEG', [
    RegexPhrase(r'\b(without)\b'),
    RegexPhrase(r'\b(not)\b'),
    RegexPhrase(r'\b(no)\b'),
])

transition_tags = _map_regex_phrases('TRANS', [
    RegexPhrase(r'\b(however)\b'),
    RegexPhrase(r'\b(but)\b'),
])

tags_mapper = {
    'negatives': negative_tags,
    'transitions': transition_tags,
}

available_tag_keys = set(tags_mapper.keys())

negative_scopes = [
    Scope(
        applied_tag='FRW-NEG',
        scope_direction=ScopeDirection.RIGHT,
        order=1,
        stop_when=['TRANS']
    )
]

scope_mapper = {
    'negatives': negative_scopes
}

available_scope_keys = set(scope_mapper.keys())

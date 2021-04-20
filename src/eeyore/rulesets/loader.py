from typing import Generator, List
from ..models import Tag, Scope
from .collection import tags_mapper, scope_mapper


def load_tags(tag_types: List[str]) -> Generator[Tag, None, None]:
    for tag_type in tag_types:
        for tag in tags_mapper[tag_type]:
            yield tag


def load_scopes(scope_types: List[str]) -> Generator[Scope, None, None]:
    for scope_type in scope_types:
        for scope in scope_mapper[scope_type]:
            yield scope

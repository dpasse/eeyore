from abc import ABC
from typing import Generator, List, Optional, Tuple
import networkx as nx
from spacy.tokens import Doc
from ..integrations import SpacyIntegration
from ..models import Context, KBTriple
from .tag_extract import TagExtract
from ..utils import iob2
from ..networks import graph


class AbsRelationshipExtract(ABC):
    @staticmethod
    def _extract_relationship(G: nx.Graph,
                              e1_tags,
                              e2_tags,
                              window_size: Optional[int] = None) \
            -> List[tuple]:
        e1_indexes = [index for index, _ in e1_tags]
        for e1_index in e1_indexes:

            e2_indexes = [index for index, _ in e2_tags]
            for e2_index in e2_indexes:
                if window_size is not None:
                    if abs(e1_index - e2_index) > window_size:
                        continue

                path: List[str] = []

                try:
                    path = graph.shortest_path(
                        G,
                        e1_index,
                        e2_index
                    )

                    path = list(set(path))

                    entity_index_space = []
                    entity_index_space.extend(e1_indexes)
                    entity_index_space.extend(e2_indexes)

                    return (
                        e1_indexes,
                        e2_indexes,
                        [
                            i
                            for i in path
                            if i not in entity_index_space
                        ]
                    )

                except:
                    # swallow, as no path exists if except exists
                    pass

        return None

    @staticmethod
    def _format_tokens(doc, ids: List[int]) -> str:
        return ' '.join(
            [doc[i].text for i in sorted(ids)]
        )

    @staticmethod
    def _get_nodes_and_edges(doc: Doc) \
            -> Tuple[List[int], List[Tuple[int, int]]]:
        nodes: List[int] = []
        edges: List[Tuple[int, int]] = []
        for token in doc:
            parent_index = token.i

            for child in token.children:
                child_index = child.i

                nodes.append(child_index)
                edges.append(
                    (parent_index, child_index),
                )

            nodes.append(parent_index)

        return list(sorted(set(nodes))), edges

    @staticmethod
    def _relationship_entities_exist(tags: dict,
                                     valid_tags: List[str]) -> bool:
        for valid_tag in valid_tags:
            if valid_tag not in tags:
                return False

        return True

    @staticmethod
    def _pull_additional_relatives(tokens: list) \
            -> Generator[int, None, None]:
        for token in tokens:
            for child in token.children:
                if child.dep_ in ['amod', 'advmod', 'neg']:
                    yield child.i

    @staticmethod
    def _determine_relationship_path(doc: Doc,
                                     e1s: List[int],
                                     e2s: List[int],
                                     relations: List[int]) -> List[str]:
        items: List[int] = relations.copy()

        items.extend(
            list(
                AbsRelationshipExtract._pull_additional_relatives(
                    [doc[i] for i in e1s]
                )
            )
        )

        items.extend(
            list(
                AbsRelationshipExtract._pull_additional_relatives(
                    [doc[i] for i in e2s]
                )
            )
        )

        # compress to unique items
        return list(set(items))


class SingleDependencyRelationshipExtract(AbsRelationshipExtract):
    def __init__(self,
                 spacy: SpacyIntegration,
                 attribute: str,
                 relationship: Tuple[str, str, str],
                 allowed_window_size: Optional[int] = None):
        self.__spacy = spacy
        self.__e1, self.__rel, self.__e2 = relationship

        self.__e1 = iob2.clean_tag(self.__e1)
        self.__e2 = iob2.clean_tag(self.__e2)

        self.__tagger = TagExtract(
            attribute,
            valid_tags=[
                self.__e1,
                self.__e2
            ]
        )

        self.__allowed_window_size_between_entities = allowed_window_size

    def evaluate(self, context: Context) -> List[KBTriple]:
        def build_relationship_combinations(tags) -> List[Tuple[str, str]]:
            combination: List[Tuple[str, str]] = []

            for e1_entity in tags[self.__e1]:
                for e2_entity in tags[self.__e2]:
                    combination.append((e1_entity, e2_entity))

            return combination

        tags = self.__tagger.evaluate(context)
        if not self._relationship_entities_exist(
            tags,
            self.__tagger.valid_tags
        ):
            return []

        doc: Doc = self.__spacy.load(context)
        G = graph.create_graph(
            *self._get_nodes_and_edges(doc),
            make_undirected=True
        )

        extracted_relationships: List[KBTriple] = []
        for e1, e2 in build_relationship_combinations(tags):

            relationship = self._extract_relationship(
                G,
                e1,
                e2,
                self.__allowed_window_size_between_entities
            )
            if relationship is None:
                continue

            e1s, e2s, relations = relationship
            items: List[int] = self._determine_relationship_path(
                doc,
                e1s,
                e2s,
                relations
            )

            extracted_relationships.append(KBTriple(
                subj=self._format_tokens(doc, e1s),
                rel=self._format_tokens(doc, items),
                obj=self._format_tokens(doc, e2s),
                cache={
                    'rel_entity': self.__rel,
                    'subj_entity': self.__e1,
                    'obj_entity': self.__e2,
                    'type': 'dependency relation',
                    'subj_indexes': e1s,
                    'rel_indexes': items,
                    'obj_indexes': e2s
                }
            ))

        return extracted_relationships


class ExpandTripleDependencyRelationshipExtract(AbsRelationshipExtract):
    def __init__(self,
                 spacy: SpacyIntegration,
                 attribute: str,
                 relationship: Tuple[str, str, str],
                 allowed_window_size: Optional[int] = None):
        self.__spacy = spacy
        self.__e1, self.__rel, self.__e2 = relationship
        self.__e2 = iob2.clean_tag(self.__e2)

        self.__tagger = TagExtract(
            attribute,
            valid_tags=[self.__e2]
        )

        self.__allowed_window_size_between_entities = allowed_window_size

    def evaluate(self,
                 triple_to_expand: KBTriple,
                 context: Context) -> List[KBTriple]:
        extracted_relationships: List[KBTriple] = []
        tags = self.__tagger.evaluate(context)
        if not self._relationship_entities_exist(
            tags,
            self.__tagger.valid_tags
        ):
            return extracted_relationships

        doc: Doc = self.__spacy.load(context)
        G = graph.create_graph(
            *self._get_nodes_and_edges(doc),
            make_undirected=True
        )

        e1_indexes = triple_to_expand.cache['obj_indexes']
        e1_tags = list(
            zip(e1_indexes, [doc[i] for i in e1_indexes])
        )

        for e2 in tags[self.__e2]:
            relationship = self._extract_relationship(
                G,
                e1_tags,
                e2,
                self.__allowed_window_size_between_entities
            )

            if relationship is None:
                break

            e1s, e2s, relations = relationship
            items: List[int] = self._determine_relationship_path(
                doc,
                e1s,
                e2s,
                relations
            )

            extracted_relationships.append(
                KBTriple(
                    subj=self._format_tokens(doc, e1s),
                    rel=self._format_tokens(doc, items),
                    obj=self._format_tokens(doc, e2s),
                    cache={
                        'rel_entity': self.__rel,
                        'subj_entity': self.__e1,
                        'obj_entity': self.__e2,
                        'type': 'dependency relation',
                        'subj_indexes': e1s,
                        'rel_indexes': items,
                        'obj_indexes': e2s
                    }
                )
            )

        return extracted_relationships


class StrictDependencyRelationshipExtract(AbsRelationshipExtract):
    def __init__(self,
                 spacy: SpacyIntegration,
                 attribute: str,
                 relationships: List[Tuple[str, str, str]],
                 allowed_window_size: Optional[int] = None):
        self.__single = SingleDependencyRelationshipExtract(
            spacy,
            attribute,
            relationships[0],
            allowed_window_size
        )

        self.__expanders = [
            ExpandTripleDependencyRelationshipExtract(
                spacy,
                attribute,
                relationship,
                allowed_window_size
            )
            for relationship in relationships[1:]
        ]

    def evaluate(self, context: Context) -> List[List[KBTriple]]:
        extracted_relationships = []
        for triple in self.__single.evaluate(context):
            relationships = [
                [triple]
            ]

            for expander in self.__expanders:

                new_relationships = []
                for relationship in relationships:
                    expanded_triples = expander.evaluate(
                        relationship[-1],
                        context
                    )
                    if len(expanded_triples) == 0:
                        relationships = []
                        break

                    for expanded_triple in expanded_triples:
                        new_relationship = relationship.copy()
                        new_relationship.append(expanded_triple)

                        new_relationships.append(new_relationship)

                relationships = new_relationships

            if len(relationships) > 0:
                extracted_relationships.extend(relationships)

        return extracted_relationships


class StaticParentRelationshipExtract(AbsRelationshipExtract):
    def __init__(self,
                 relationship: Tuple[str, str, str]):
        self.__e1, self.__rel, self.__e2 = relationship
        self.__e1 = iob2.clean_tag(self.__e1)
        self.__e2 = iob2.clean_tag(self.__e2)

    def evaluate(self, triples: List[KBTriple], static_value: str) -> List[KBTriple]:
        collection: List[KBTriple] = []
        for triple in triples:
            collection.append(triple)

            if triple.cache['subj_entity'] == self.__e2:
                collection.append(KBTriple(
                    rel='',
                    subj=static_value,
                    obj=triple.subj,
                    cache={
                        'rel_entity': self.__rel,
                        'subj_entity': self.__e1,
                        'obj_entity': self.__e2,
                        'type': 'static parent',
                        'subj_indexes': [],
                        'rel_indexes': [],
                        'obj_indexes': triple.cache['subj_indexes']
                    }
                ))

        return collection

from typing import Generator, List, Optional, Tuple
import networkx as nx
from spacy.tokens import Doc
from ..integrations import SpacyIntegration
from ..models import Context, KBTriple
from .tag_extract import TagExtract
from ..utils import iob2
from ..networks import graph


class DependencyRelationshipExtract():
    def __init__(self,
                 spacy: SpacyIntegration,
                 attribute: str,
                 e1: str,
                 e2: str,
                 rel: str,
                 allowed_window_size: Optional[int] = None):
        self.__spacy = spacy
        self.__e1 = iob2.clean_tag(e1)
        self.__e2 = iob2.clean_tag(e2)
        self.__rel = rel
        self.__tagger = TagExtract(
            attribute,
            valid_tags=[
                self.__e1,
                self.__e2
            ]
        )
        self.__dep_attributes_to_append = [
            'amod',
            'advmod',
            'neg'
        ]
        self.__allowed_window_size_between_entities = allowed_window_size

    def evaluate(self, context: Context) -> List[KBTriple]:
        relationships = []

        tags = self.__tagger.evaluate(context)
        if self._validate_extracted_tags(tags):
            return relationships

        doc: Doc = self.__spacy.load(context)
        nodes, edges = self._get_nodes_and_edges(doc)
        G = graph.create_graph(nodes, edges, make_undirected=True)

        for e1s, e2s, relations in self._extract_relationships(G, tags):
            items: List[int] = self._determine_relationship_path(
                doc,
                e1s,
                e2s,
                relations
            )

            triple = KBTriple(
                subj=self._format_tokens(doc, e1s),
                rel=self._format_tokens(doc, items),
                obj=self._format_tokens(doc, e2s),
            )

            triple.update_cache({
                'rel_entity': self.__rel,
                'subj_entity': self.__e1,
                'obj_entity': self.__e2,
                'type': 'dependency relation',
                'subj_indexes': e1s,
                'rel_indexes': items,
                'obj_indexes': e2s
            })

            relationships.append(triple)

        return relationships

    def _extract_relationships(self, G: nx.Graph, tags: dict) -> List[tuple]:
        def get_combos(tags):
            for e1_tags in tags[self.__e1]:
                for e2_tags in tags[self.__e2]:
                    yield (e1_tags, e2_tags)

        valid_paths: List[tuple] = []
        for e1_tags, e2_tags in get_combos(tags):
            valid_path: tuple = None

            e1_indexes = [index for index, _ in e1_tags]
            for e1_index in e1_indexes:

                e2_indexes = [index for index, _ in e2_tags]
                for e2_index in e2_indexes:
                    if self.__allowed_window_size_between_entities is not None:
                        if abs(e1_index - e2_index) > \
                                self.__allowed_window_size_between_entities:
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

                        valid_path = (
                            e1_indexes,
                            e2_indexes,
                            [
                                i
                                for i in path
                                if i not in entity_index_space
                            ]
                        )

                        break
                    except:
                        # swallow, as no path exists if except exists
                        pass

                if valid_path is not None:
                    break

            if valid_path is not None:
                valid_paths.append(valid_path)

        return valid_paths

    def _get_nodes_and_edges(self,
                             doc: Doc) \
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

    def _validate_extracted_tags(self, tags: dict) -> bool:
        return self.__e1 not in tags or self.__e2 not in tags

    def _pull_additional_relatives(self,
                                   tokens: list) \
            -> Generator[int, None, None]:
        for token in tokens:
            for child in token.children:
                if child.dep_ in self.__dep_attributes_to_append:
                    yield child.i

    def _determine_relationship_path(self,
                                     doc: Doc,
                                     e1s: List[int],
                                     e2s: List[int],
                                     relations: List[int]) -> List[str]:
        items: List[int] = relations.copy()

        items.extend(
            list(
                self._pull_additional_relatives(
                    [doc[i] for i in e1s]
                )
            )
        )

        items.extend(
            list(
                self._pull_additional_relatives(
                    [doc[i] for i in e2s]
                )
            )
        )

        # compress to unique items
        return list(set(items))

    @staticmethod
    def _format_tokens(doc, ids: List[int]) -> str:
        return ' '.join(
            [doc[i].text for i in sorted(ids)]
        )


class OneSidedRelationshipExtract():
    def __init__(self,
                 spacy: SpacyIntegration,
                 attribute: str,
                 side_of_relation: str,
                 e1: str,
                 e2: str,
                 rel: str):
        self.__spacy = spacy
        self.__e1 = iob2.clean_tag(e1)
        self.__e2 = iob2.clean_tag(e2)
        self.__rel = rel

        self.__valid_tag = self.__e1 \
            if side_of_relation == 'e1' \
            else self.__e2

        self.__tagger = TagExtract(
            attribute,
            valid_tags=[
                self.__valid_tag
            ]
        )

        self.__side_of_relation = side_of_relation
        self.__dep_attributes_to_append = [
            'amod',
            'advmod',
            'neg'
        ]

    def evaluate(self, context: Context, static_value: str) -> List[KBTriple]:
        relationships = []

        tags = self.__tagger.evaluate(context)
        if self.__valid_tag not in tags:
            return relationships

        doc: Doc = self.__spacy.load(context)

        if self.__side_of_relation == 'e1':
            for tags in tags[self.__e1]:
                indexes = [i for i, _ in tags]
                relations = list(
                    self._pull_additional_relatives(
                        [doc[i] for i in indexes]
                    )
                )

                triple = KBTriple(
                    subj=self._format_tokens(doc, indexes),
                    rel=self._format_tokens(doc, relations),
                    obj=static_value,
                )

                triple.update_cache({
                    'rel_entity': self.__rel,
                    'subj_entity': self.__e1,
                    'obj_entity': self.__e2,
                    'type': '1-sided w/ obj static',
                    'rel_indexes': relations,
                    'subj_indexes': indexes
                })

                relationships.append(triple)
        else:
            for tags in tags[self.__e2]:
                indexes = [i for i, _ in tags]
                relations = list(
                    self._pull_additional_relatives(
                        [doc[i] for i in indexes]
                    )
                )

                triple = KBTriple(
                    subj=static_value,
                    rel=self._format_tokens(doc, relations),
                    obj=self._format_tokens(doc, indexes),
                )

                triple.update_cache({
                    'rel_entity': self.__rel,
                    'subj_entity': self.__e1,
                    'obj_entity': self.__e2,
                    'type': '1-sided w/ subj static',
                    'rel_indexes': relations,
                    'obj_indexes': indexes
                })

                relationships.append(triple)

        return relationships

    def _pull_additional_relatives(self,
                                   tokens: list) \
            -> Generator[int, None, None]:
        for token in tokens:
            for child in token.children:
                if child.dep_ in self.__dep_attributes_to_append:
                    yield child.i

    @staticmethod
    def _format_tokens(doc, ids: List[int]) -> str:
        return ' '.join(
            [doc[i].text for i in sorted(ids)]
        )

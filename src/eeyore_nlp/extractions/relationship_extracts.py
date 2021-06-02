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
                 relationships: List[Tuple[str, str, str]],
                 allowed_window_size: Optional[int] = None):
        self.__spacy = spacy
        self.__relationships = [
            (
                iob2.clean_tag(e1),
                rel,
                iob2.clean_tag(e2)
            )
            for e1, rel, e2 in relationships
        ]

        valid_tags = set()
        for e1, _, e2 in self.__relationships:
            valid_tags.add(e1)
            valid_tags.add(e2)

        self.__tagger = TagExtract(
            attribute,
            valid_tags=list(valid_tags)
        )

        self.__dep_attributes_to_append = [
            'amod',
            'advmod',
            'neg'
        ]
        self.__allowed_window_size_between_entities = allowed_window_size

    def evaluate(self, context: Context):
        def build_relationship_combinations(tags):
            def get_new_combination(combination, entities, rel='<END>'):
                new_combination = []
                for combo in combination:
                    for entity in entities:
                        new_combination.append((*combo, entity, rel))

                return new_combination

            combination = []
            e1, rel, e2 = self.__relationships[0]
            for entity in tags[e1]:
                combination.append(
                    (entity, rel)
                )

            for i in range(1, len(self.__relationships)):
                e1, rel, e2 = self.__relationships[i]
                combination = get_new_combination(combination, tags[e1], rel)

            return get_new_combination(combination, tags[e2])

        tags = self.__tagger.evaluate(context)
        if not self._relationship_entities_exist(tags):
            return []

        doc: Doc = self.__spacy.load(context)
        nodes, edges = self._get_nodes_and_edges(doc)
        G = graph.create_graph(nodes, edges, make_undirected=True)

        extracted_relationships = []
        for combination in build_relationship_combinations(tags):

            i = 0
            extracted_combination = []

            while True:
                e1 = combination[0]
                e2 = combination[2]

                relationship = self._extract_relationship(G, e1, e2)
                if relationship is None:
                    break

                e1s, e2s, relations = relationship
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

                e1_entity, rel, e2_entity = self.__relationships[i]
                triple.update_cache({
                    'rel_entity': rel,
                    'subj_entity': e1_entity,
                    'obj_entity': e2_entity,
                    'type': 'dependency relation',
                    'subj_indexes': e1s,
                    'rel_indexes': items,
                    'obj_indexes': e2s
                })

                extracted_combination.append(triple)

                i += 1
                combination = combination[2:]

                if len(combination) < 3:
                    break

            if len(extracted_combination) == len(self.__relationships):
                extracted_relationships.append(
                    extracted_combination.copy()
                )

        return extracted_relationships

    def _extract_relationship(self,
                              G: nx.Graph,
                              e1_tags,
                              e2_tags) -> List[tuple]:
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

    def _relationship_entities_exist(self, tags: dict) -> bool:
        for valid_tag in self.__tagger.valid_tags:
            if valid_tag not in tags:
                return False

        return True

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

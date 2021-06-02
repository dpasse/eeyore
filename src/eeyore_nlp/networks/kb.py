from typing import Dict, Optional
import networkx as nx


def add_knowledge(G: nx.DiGraph,
                  parent: str,
                  relationship: str,
                  child: str):
    args = {
        relationship: True
    }

    G.add_edge(
        parent.lower(),
        child.lower(),
        **args
    )


class KnowledgeBase():
    def __init__(self,
                 kb: nx.DiGraph,
                 node_alias: Optional[Dict[str, str]]) -> None:
        self.__kb = kb
        self.__node_alias: Dict[str, str] = {}

        if node_alias is not None:
            self.__node_alias.update(node_alias)

    def validate_relationship(self,
                              parent: str,
                              by_rel: str,
                              child: str) -> bool:
        parent_node = self._clean_node(parent)
        child_node = self._clean_node(child)

        try:
            return by_rel in self.__kb.edges[parent_node, child_node]
        except:
            pass

        return False

    def _clean_node(self, node: str) -> str:
        return (
            self.__node_alias[node]
            if node in self.__node_alias
            else node
        ).lower()

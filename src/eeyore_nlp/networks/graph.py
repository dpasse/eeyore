from typing import List, Set, Tuple
import networkx as nx
from ..models import RelationshipContainer, Context


def create(relationship_container: RelationshipContainer,
           make_undirected: bool = True) -> nx.Graph:
    nodes: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()

    for parent, relationship in relationship_container.items():
        nodes.add(parent.term)

        for child in relationship.children:
            nodes.add(child.term)
            edges.add((parent.term, child.term))

    G = nx.Graph() if not make_undirected else nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


def shortest_path(G, source: str, target: str) -> List[str]:
    return nx.shortest_path(G, source, target)


def get_edges_from_adjacent_terms(tokens: List[str]) -> List[Tuple[str, str]]:
    if len(tokens) == 0:
        return []

    return [
        (
            tokens[i-1],
            tokens[i]
        )
        for i in range(1, len(tokens))
    ]


def append_terms_to_graph(G, context: Context) -> nx.Graph:
    edges = get_edges_from_adjacent_terms(
        context.get('tokens')
    )

    G.add_edges_from(edges)

    return G

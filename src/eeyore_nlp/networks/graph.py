from typing import List, Set, Tuple
import networkx as nx
from ..models import RelationshipContainer


def create(relationship_container: RelationshipContainer,
           make_undirected: bool = True) -> nx.Graph:
    nodes: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()

    for parent, relationship in relationship_container.items():
        nodes.add(parent)

        for child in relationship.children:
            nodes.add(child)
            edges.add((parent, child))

    G = nx.Graph() if not make_undirected else nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return G


def shortest_path(G, source: str, target: str) -> List[str]:
    return nx.shortest_path(G, source, target)

"""
To generate minimum spanning tree of a Undirected Graph. This graph should be
connected.
"""
from .graph_data_structre import UndirectedGraph


def prim(graph: UndirectedGraph):
    """
    Use prim algorithm to generate minimum spanning tree of a undirected graph.
    This undirected graph should be connected.

    Args:
        graph: a UndirectedGraph object.
    """
    if not isinstance(graph, UndirectedGraph):
        raise TypeError('Should be a UndirectedGraph object.')
    graph.cal_adjacency_matrix()

    mmtree_V = set()
    mmtree_E = set()

    nodes = graph._V.copy()

    node = nodes.pop()
    mmtree_V.add(node)
    while nodes:
        another_node, nearest_edge = _get_nearest_edge(mmtree_V, nodes, graph)
        mmtree_V.add(another_node)
        mmtree_E.add(nearest_edge)
        nodes.remove(another_node)
    return mmtree_V, mmtree_E


def _get_nearest_edge(nodes1, nodes2, graph: UndirectedGraph):
    """
    Find which edge of nodes2 is the nearest to nodes1.

    Args:
    """

    target_node = None
    target_edge = None

    for node1 in nodes1:
        for node2 in nodes2:
            weight, edge = graph.get_weight_of_edge(node1, node2)
            if target_edge is None or target_edge > weight:
                target_node = node2
                target_edge = edge
    return target_node, target_edge

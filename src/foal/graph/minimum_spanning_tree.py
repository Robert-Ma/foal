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

    mstree_V = set()
    mstree_E = set()

    nodes = graph._V.copy()

    node = nodes.pop()
    mstree_V.add(node)
    while nodes:
        another_node, nearest_edge = _get_nearest_edge(mstree_V, nodes, graph)
        mstree_V.add(another_node)
        mstree_E.add(nearest_edge)
        nodes.remove(another_node)
    return mstree_V, mstree_E


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


def kruskal(graph: UndirectedGraph):
    """
    Kruskal's algorithm for the Minimum Spanning Tree problem starts by
    creating disjoint subsets of V, one for each vertex and containing only
    that vertex. It then inspects the edges according to nondecreasing weight
    (ties are broken arbitraily). If an edge connects two vertices in disjoint
    subsets, the edge is added and the subsets are merged into one set. This
    process is repeated until all the subsets are mergred into one set.
    """

    if not isinstance(graph, UndirectedGraph):
        raise TypeError('Should be a UndirectedGraph object.')

    if not _is_acyclic(graph.get_edges()):
        return graph.get_nodes(), graph.get_edges()

    all_edges_of_graph = sorted(list(graph.get_edges()), reverse=False)  # list
    all_nodes_of_graph = graph.get_nodes()   # set()

    mstree_V = set()
    mstree_E = set()

    while all_edges_of_graph:
        edge = all_edges_of_graph.pop(0)

        temp_mstree_E = mstree_E.copy()
        temp_mstree_E.add(edge)
        if not _is_acyclic(temp_mstree_E):
            mstree_E.add(edge)
            node1, node2 = edge.get_nodes()
            mstree_V.add(node1)
            mstree_V.add(node2)

            if all_nodes_of_graph == mstree_V:
                break
    return mstree_V, mstree_E


def _is_acyclic(edges: set):
    """
    Use the number of nodes (NN) and the number of edges (NE) to determine
    whether an undirected graph has a ring:
        NE >= NN: has a ring
        NE < NN: does not have a ring

    Args:
        edges: a set of Edge.
    """
    NE = len(edges)

    nodes = set()

    for edge in edges:
        node1, node2 = edge.get_nodes()
        nodes.add(node1)
        nodes.add(node2)

    NN = len(nodes)

    return True if NE >= NN else False

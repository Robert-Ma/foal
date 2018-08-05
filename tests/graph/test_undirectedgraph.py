import numpy as np
import pytest

from foal.graph import Edge, UndirectedGraph


@pytest.fixture(name='graph')
def pre_graph():
    ug = UndirectedGraph()
    ug.add_edge(1, 2, 0.1)
    ug.add_edge(2, 3, 0.2)
    ug.add_edge(2, 4, 0.1)
    ug.add_edge(3, 4, 0.4)
    return ug


def test_graph_add_edge():
    ug = UndirectedGraph()
    ug.add_edge(1, 2, 0.1)
    assert ug._V == {1, 2} and ug._E == set([Edge(1, 2, 0.1)])


def test_add_negitive_integer():
    ug = UndirectedGraph()
    with pytest.raises(ValueError):
        ug.add_edge(-1, 2, 0.2)


def test_add_float():
    ug = UndirectedGraph()
    with pytest.raises(ValueError):
        ug.add_edge(0.1, 2, 0.2)


def test_adjacency_matrix(graph):
    graph.cal_adjacency_matrix()
    adj_mat = graph.get_adjacency_matrix()

    expected_mat = np.zeros((5, 5))
    expected_mat[:] = float('inf')

    expected_mat[1, 2] = 0.1
    expected_mat[2, 1] = 0.1
    expected_mat[2, 3] = 0.2
    expected_mat[3, 2] = 0.2
    expected_mat[2, 4] = 0.1
    expected_mat[4, 2] = 0.1
    expected_mat[3, 4] = 0.4
    expected_mat[4, 3] = 0.4
    expected_mat[1, 1] = 0.0
    expected_mat[2, 2] = 0.0
    expected_mat[3, 3] = 0.0
    expected_mat[4, 4] = 0.0
    assert np.array_equal(adj_mat, expected_mat)


def test_node_wiht_one_edge(graph):
    node = graph.get_node_with_only_one_edge()
    assert node == set([1, ])


def test_edge_of_node(graph):
    edges = graph.get_edges_of_node(1)

    expected = set([Edge(1, 2, 0.1)])
    assert edges == expected


def test_nearest_edge(graph):
    node, edge = graph.get_nearest_edge_of_node(4)
    assert node == 2 and edge == Edge(2, 4, 0.1)

"""
An undirected graph G consists of a finite set V whose members are called
vertices of G, together with a set E of pairs of vertices in V. These pairs are
called the edges of G. Denote G by
                           G = (V, E)
"""

import operator
from collections import Counter

import numpy as np


class Edge:
    """
    The edges of an undirected graph.

    Edge consists of Nodes and weight.
    """

    def __init__(self, node_name_1, node_name_2, weight):
        """
        Args:
            node_name_1, node_name_2: integer, the names of the nodes at both
                                      ends of the edge.
            weight: float or int
        """
        if node_name_1 == node_name_2:
            raise ValueError(" two nodes should not be same.")
        self._nodes = (node_name_1, node_name_2)
        self._weight = weight

    def get_nodes(self):
        """
        Get all nodes' name

        return:
            tuple()
        """
        return self._nodes

    def has_node(self, node_name):
        """
        Determine if this edge contains given node.
        """
        return True if node_name in self._nodes else False

    def get_another_node(self, node_name):
        """
        Get another node of edge.
        """
        if self.has_node(node_name):
            # A Edge object just contains two nodes
            set_of_nodes = set(self._nodes)
            diff = set_of_nodes.difference(set((node_name,)))
            another_node_name = diff.pop()
            return another_node_name
        else:
            raise ValueError('This edge does not contain Node: %s' % node_name)

    def get_weight(self):
        return self._weight

    def __repr__(self):
        return '{}<-->{}: {}'.format(self._nodes[0], self._nodes[1],
                                     self._weight)

    def __str__(self):
        return '{}'.format(self._weight)

    def __contains__(self, node_name):
        """
        Determine if this edge contains node_name
        Args:
            node_name: integer
        """
        if not isinstance(node_name, int):
            raise TypeError('require a integer prameter.')
        return True if node_name in self._nodes else False

    def __eq__(self, other):
        return self._compare(operator.eq, other)

    def __ne__(self, other):
        return self._compare(operator.ne, other)

    def __ge__(self, other):
        return self._compare(operator.ge, other)

    def __gt__(self, other):
        return self._compare(operator.gt, other)

    def __le__(self, other):
        return self._compare(operator.le, other)

    def __lt__(self, other):
        return self._compare(operator.lt, other)

    def __hash__(self):
        return hash((self._nodes, self._weight))

    def _is_a_edge(self, other):
        if isinstance(other, self.__class__):
            return True
        elif isinstance(other, (int, float)):
            return False
        else:
            raise TypeError('another object should be Edge, integer or float.')

    def _compare(self, oper, other):
        if self._is_a_edge(other):
            return True if oper(self._weight, other._weight) else False
        else:
            return True if oper(self._weight, other) else False


class UndirectedGraph:
    """
    Weighted Undirected Graph
    """
    def __init__(self):
        self._V = set()   # nodes, integers
        self._E = set()   # edges, Edge objects
        self._adjacency_mat = None   # np.matrix

    def add_edge(self, node1, node2, weight):
        """
        Args:
            node1, node2: int, node name
            weight: float
        """
        self._check_node_name_type(node1)
        self._check_node_name_type(node2)

        self._V.add(node1)
        self._V.add(node2)
        self._E.add(Edge(node1, node2, weight))

    def get_edges(self):
        """Get all edges"""
        return self._E

    def get_nodes(self):
        """Get all nodes"""
        return self._V

    def cal_adjacency_matrix(self):
        """
        Calculate adjacency matrix of graph.
        """
        if len(self._V) == 0:
            raise ValueError('Graph should contain at less one node.')
        self._adjacency_mat = np.zeros((max(self._V) + 1, max(self._V) + 1))
        self._adjacency_mat[:] = float('inf')

        for edge in self._E:
            node1, node2 = edge.get_nodes()
            weight = edge.get_weight()
            self._adjacency_mat[node1, node2] = weight
            self._adjacency_mat[node2, node1] = weight

        for node in self._V:
            self._adjacency_mat[node, node] = 0.

    def get_adjacency_matrix(self):
        return self._adjacency_mat

    def get_node_with_only_one_edge(self):
        """
        Get nodes which just have one edge.

        Return:
            nodes_with_one_edge: set()
        """
        node_counter = Counter()
        nodes_with_one_edge = set()
        for edge in self._E:
            node1, node2 = edge.get_nodes()
            node_counter[node1] += 1
            node_counter[node2] += 1
        for node in node_counter.keys():
            if node_counter[node] == 1:
                nodes_with_one_edge.add(node)
        return nodes_with_one_edge

    def get_edges_of_node(self, node):
        """
        Get all edges whose one node is given node.

        Return
            edges: set()
        """
        self._is_right_node_name(node)

        edges = set()
        for edge in self._E:
            if node in edge:
                edges.add(edge)
        return edges

    def get_nearest_edge_of_node(self, node):
        """
        Get the edge nearest to a node.
        """
        self._is_right_node_name(node)

        all_edges = self.get_edges_of_node(node)
        nearest_edge = min(all_edges)
        another_node = nearest_edge.get_another_node(node)

        return another_node, nearest_edge

    def get_weight_of_edge(self, node1, node2):
        self._is_right_node_name(node1)
        self._is_right_node_name(node2)

        weight = self._adjacency_mat[node1, node2]
        return weight, self.get_edge_of_two_nodes(node1, node2)

    def get_edge_of_two_nodes(self, node1, node2):
        self._is_right_node_name(node1)
        self._is_right_node_name(node2)

        for edge in self._E:
            if node1 in edge and node2 in edge:
                return edge
        return None

    def _is_right_node_name(self, node):
        self._check_node_name_type(node)

        if self._V:
            if node < min(self._V) or node > max(self._V):
                raise ValueError('No such Node.')
        else:
            return True

    def _check_node_name_type(self, node):
        if not isinstance(node, int) or node < 0.:
            raise TypeError('Node should be positive integer.')
        else:
            return True


class DirectedGraph:
    """
    Weighted Directed Graph.
    """
    pass

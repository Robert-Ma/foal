"""
An undirected graph G consists of a finite set V whose members are called
vertices of G, together with a set E of pairs of vertices in V. These pairs are
called the edges of G. Denote G by
                           G = (V, E)
"""

import numpy as np
from collections import Counter


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
        return True if self._weight == other._weight else False

    def __ne__(self, other):
        return True if self._weight != other._weight else False

    def __ge__(self, other):
        return True if self._weight >= other._weight else False

    def __gt__(self, other):
        return True if self._weight > other._weight else False

    def __le__(self, other):
        return True if self._weight <= other._weight else False

    def __lt__(self, other):
        return True if self._weight < other._weight else False

    def __hash__(self):
        return hash((self._nodes, self._weight))


class UndirectedGraph:
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
        self._is_right_node_name(node1)
        self._is_right_node_name(node2)

        self._V.add(node1)
        self._V.add(node2)
        self._E.add(Edge(node1, node2, weight))

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
        Get the nearest edge of a node.
        """
        self._is_right_node_name(node)

        all_edges = self.get_edges_of_node(node)
        nearest_edge = min(all_edges)
        another_node = nearest_edge.get_another_node(node)

        return another_node, nearest_edge

    def _is_right_node_name(self, node):
        if not isinstance(node, int) or node < 0.:
            raise ValueError('Node should be positive integer.')
        else:
            return True

"""
Dijkstra's Algorithm

Determine the shortest paths from `node v1` to all other vertices in a
weighted, directed graph.
"""
from collections import defaultdict

from .graph_data_structre import DirectedGraph


class Dijkstra:
    """
    Dijkstra's Algorithm

    Determine the shortest paths from starting node `node v1` to all other
    vertices in a weighted, directed graph.

    `graph` should has only one starting node, and has only one ending node,
    and its weights should be positive float.
    """
    def __init__(self, graph: DirectedGraph):
        self._is_weight_positive(graph)
        self._has_only_one_starting_node(graph)
        self._has_only_one_ending_node(graph)

        self._graph = graph

        # a dict of dict: {1: {'parent': 2, 'weight': 3}}
        self._min_weights = defaultdict(lambda: {'parent': None,
                                                 'weight': float('inf')})
        self._child_to_cal = list()
        self._child_already_cal = set()

    def display_shortesst_path(self, end_node=None):
        if end_node:
            self._is_right_node_name(end_node)
            node = end_node
        else:
            node = self._graph.get_end_node()
        path = list()
        while node is not None:
            path.append(node)
            node = self._min_weights[node]['parent']
        path.reverse()
        print(path)
        path.clear()

    def get_all_info_of_shortest_path(self):
        return self._min_weights

    def cal_shortest_path(self, start_node=None):
        if not start_node:
            node = self._graph.get_start_node()[0]
        else:
            node = start_node
        self._update_child_to_cal(node)
        self._min_weights[node]['weight'] = 0.

        while len(self._child_to_cal):
            node = self._child_to_cal.pop(0)
            self._cal_weight_to_child(node)

    def _cal_weight_to_child(self, cur_node):
        self._is_right_node_name(cur_node)

        edges_start_with_cur_node = self._graph.get_edges_start_with(cur_node)
        if not edges_start_with_cur_node:
            return

        for edge in edges_start_with_cur_node:
            weight = edge.get_weight()
            last_node = edge.get_last_node()
            self._update_child_to_cal(last_node)

            self._update_min_weights(cur_node, last_node, weight)

        self._update_child_already_cal(cur_node)

    def _update_min_weights(self, cur_node, child_node, weight):
        self._is_right_node_name(cur_node)
        self._is_right_node_name(child_node)

        parent_weight = self._min_weights[cur_node]['weight']
        new_weight = parent_weight + weight
        old_weight = self._min_weights[child_node]['weight']

        if new_weight < old_weight:
            self._min_weights[child_node]['parent'] = cur_node
            self._min_weights[child_node]['weight'] = new_weight

    def _update_child_to_cal(self, node):
        self._is_right_node_name(node)
        if node not in self._child_already_cal:
            self._child_to_cal.append(node)

    def _update_child_already_cal(self, node):
        self._is_right_node_name(node)
        self._child_already_cal.add(node)

    def _is_weight_positive(self, graph):
        weights = graph.get_weights()
        is_positive = all(map(lambda w: w >= 0., weights))

        if not is_positive:
            raise ValueError("graph's weights should be positive float.")
        else:
            return True

    def _has_only_one_starting_node(self, graph):
        starting_nodes = graph.get_start_node()
        if len(starting_nodes) == 0:
            raise ValueError('`graph` does not have starting node.')
        elif len(starting_nodes) == 1:
            return True
        else:
            return False

    def _has_only_one_ending_node(self, graph):
        end_nodes = graph.get_end_node()
        if len(end_nodes) == 0:
            raise ValueError('`graph` does not have ending node.')
        elif len(end_nodes) == 1:
            return True
        else:
            return False

    def _is_right_node_name(self, node):
        nodes = self._graph.get_nodes()

        if node < min(nodes) or node > max(nodes):
            raise ValueError('No such node.')
        else:
            return True

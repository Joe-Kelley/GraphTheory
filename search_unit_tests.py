# coding=utf-8
import pickle
import random
import unittest

import matplotlib.pyplot as plt
import networkx

from explorable_graph import ExplorableGraph
from Dijkstras import dijktras_search
from PriorityQueue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    """Test Priority Queue implementation"""

    def test_append_and_pop(self):
        """Test the append and pop functions"""
        queue = PriorityQueue()
        temp_list = []

        for _ in range(10):
            a = random.randint(0, 10000)
            queue.append((a, 'a'))
            temp_list.append(a)

        temp_list = sorted(temp_list)

        for item in temp_list:
            popped = queue.pop()
            self.assertEqual(popped[0], item)

    def test_fifo_property(self):
        "Test the fifo property for nodes with same priority"
        queue = PriorityQueue()
        temp_list = [(1,'b'), (1, 'c'), (1, 'a'), (2,'f'), (2,'d')]
        correct_list = [(1,'b'), (1, 'c'), (1, 'a'), (2,'f'), (2,'d')]

        for node in temp_list:
            queue.append(node)

        for expected_node in correct_list:
            actual_node = queue.pop()
            self.assertEqual(actual_node[-1], expected_node[-1])


class TestBasicSearch(unittest.TestCase):
    """Test the simple search algorithms: BFS, UCS, A*"""

    def setUp(self):
        """Romania map data from Russell and Norvig, Chapter 3."""
        with open('romania_graph.pickle', 'rb') as rom:
            romania = pickle.load(rom)
        self.romania = ExplorableGraph(romania)
        self.romania.reset_search()

    def test_bfs(self):
        """Test and visualize breadth-first search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path = breadth_first_search(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path,
                        title='test_bfs blue=start, yellow=goal, green=explored')

    def test_bfs_num_explored(self):
        """Test BFS for correct path and number of explored nodes"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path = breadth_first_search(self.romania, start, goal)

        self.assertEqual(['a', 's', 'f', 'b', 'u'], path)   # Check for correct path

        explored_nodes = sum(list(self.romania.explored_nodes().values()))
        self.assertLessEqual(explored_nodes, 10)    # Compare explored nodes to reference implementation

    def test_bfs_empty_path(self):
        start = "a"
        goal = "a"
        path = breadth_first_search(self.romania, start, goal)
        self.assertEqual(path, [])

    def test_ucs(self):
        """TTest and visualize uniform-cost search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path = uniform_cost_search(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path,
                        title='test_ucs blue=start, yellow=goal, green=explored')

    def test_ucs_num_explored(self):
        """Test UCS for correct path and number of explored nodes"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path = uniform_cost_search(self.romania, start, goal)

        self.assertEqual(path, ['a', 's', 'r', 'p', 'b', 'u'])   # Check for correct path

        explored_nodes = sum(list(self.romania.explored_nodes().values()))
        self.assertEqual(explored_nodes, 13)    # Compare explored nodes to reference implementation

    def test_dijkstras(self):
        """Test and visualize Dijkstra's Algo -- All node paths printed to console"""
        start = 'a'
        goal = 'n'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path_to_nodes = dijktras_search(self.romania, start, goal)
        path = None
        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path,
                        title='test_dijkstras blue=start, yellow=goal, green=explored',
                        node_paths=path_to_nodes)

    def test_a_star(self):
        """Test and visualize A* search"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path = a_star(self.romania, start, goal)

        self.draw_graph(self.romania, node_positions=node_positions,
                        start=start, goal=goal, path=path,
                        title='test_astar blue=start, yellow=goal, green=explored')

    def test_a_star_num_explored(self):
        """Test A* for correct path and number of explored nodes"""
        start = 'a'
        goal = 'u'

        node_positions = {n: self.romania.nodes[n]['pos'] for n in
                          self.romania.nodes.keys()}

        self.romania.reset_search()
        path = a_star(self.romania, start, goal)

        self.assertEqual(path, ['a', 's', 'r', 'p', 'b', 'u'])   # Check for correct path

        explored_nodes = sum(list(self.romania.explored_nodes().values()))
        self.assertEqual(explored_nodes, 8)    # Compare explored nodes to reference implementation

    @staticmethod
    def draw_graph(graph, node_positions=None, start=None, goal=None,
                   path=None, title='', node_paths={}):
        """Visualize results of graph search"""
        explored = [key for key in graph.explored_nodes() if graph.explored_nodes()[key] > 0]

        labels = {}
        for node in graph:
            labels[node] = node

        if node_positions is None:
            node_positions = networkx.spring_layout(graph)

        networkx.draw_networkx_nodes(graph, node_positions)
        networkx.draw_networkx_edges(graph, node_positions, style='dashed')
        # if node_paths:
        #     networkx.draw_networkx_labels(graph, node_positions, node_paths)
        # else:
        networkx.draw_networkx_labels(graph, node_positions, labels)

        networkx.draw_networkx_nodes(graph, node_positions, nodelist=explored,
                                     node_color='g')
        edge_labels = networkx.get_edge_attributes(graph, 'weight')
        networkx.draw_networkx_edge_labels(graph, node_positions, edge_labels=edge_labels)

        if path is not None:
            edges = [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]
            networkx.draw_networkx_edges(graph, node_positions, edgelist=edges,
                                         edge_color='b')

        if start:
            networkx.draw_networkx_nodes(graph, node_positions,
                                         nodelist=[start], node_color='b')

        if goal:
            networkx.draw_networkx_nodes(graph, node_positions,
                                         nodelist=[goal], node_color='y')

        # if node_paths:
        #     for node in node_paths:
        #         node_path = ' '.join(str(e) for e in node_paths[node])
        #         plt.text('Shortest path for Node: ', ' ')

        # if node_paths:
        #     ax2 = plt.add_subplot()

        plt.title(title)
        plt.plot()
        plt.show()



if __name__ == '__main__':
    unittest.main()

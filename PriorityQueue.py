import heapq


class PriorityQueue(object):
    def __init__(self):
        """Initialize a new Priority Queue."""

        self.queue = []

        self.append_nodes = []
        self.append_lookup = {}

        self.pop_nodes = []

        self.append_counter = 0
        self.pop_counter = 0

    # Reference: https://docs.python.org/3/library/heapq.html
    def pop(self):
        popped, i, var = heapq.heappop(self.queue)

        return popped, var

    def remove(self, node):
        count = 0
        for nodes in self.queue:
            if nodes[2] == node:
                del self.queue[count]
            count += 1

    def __iter__(self):
        """Queue iterator."""

        return iter(sorted(self.queue))

    def __str__(self):
        """Priority Queue to string."""

        return 'PQ:%s' % self.queue

    def append(self, node):
        """
        Append a node to the queue.

        Args:
            node: Comparable Object to be added to the priority queue.
        """

        node_as_list = list(node)

        node_as_list.append(self.append_counter)
        node_val = node_as_list[0]
        node_var = node_as_list[1]
        node_index = node_as_list[2]

        node_as_list = [node_val, node_index, node_var]
        self.append_lookup[self.append_counter] = node_as_list
        self.append_counter += 1

        return heapq.heappush(self.queue, node_as_list)

    def __contains__(self, key):
        """
        Containment Check operator for 'in'

        Args:
            key: The key to check for in the queue.

        Returns:
            True if key is found in queue, False otherwise.
        """

        return key in [n[-1] for n in self.queue]

    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.

        Args:
            other (PriorityQueue): Priority Queue to compare against.

        Returns:
            True if the two priority queues are equivalent.
        """

        return self.queue == other.queue

    def size(self):
        """
        Get the current size of the queue.

        Returns:
            Integer of number of items in queue.
        """

        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""

        self.queue = []

    def top(self):
        """
        Get the top item in the queue.

        Returns:
            The first item stored in the queue.
        """

        return self.queue[0]
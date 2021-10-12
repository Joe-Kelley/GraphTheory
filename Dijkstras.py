import copy
from PriorityQueue import PriorityQueue


# Return the shortest path to every Node in Graph
def dijktras_search(graph, start, goal):
    # parent node history
    parent_history = {}
    # total cost of path to node
    total_cost = {}
    # the shortest path to each node
    shortest_path = {}

    # index for nodes in queue
    index = 0

    # append our start node to our frontier
    frontier = PriorityQueue()
    frontier.append((index, start))

    # We need this to end our while loop to build the path
    parent_history[start] = False
    total_cost[start] = 0

    # While not Is-Empty(frontier) do
    while frontier.size() != 0:
        val, node = frontier.pop()
        shortest_path[node] = []
        parent_node = node
        children = graph[node]

        index += 1

        # This is where we return our path by using our parent node dictionary
        old_parent_node = copy.copy(parent_node)
        while parent_node:
            prev_lookup = parent_node
            parent_node = parent_history[prev_lookup]
            shortest_path[node].append(prev_lookup)

        # path.reverse()
        # # path.append(goal)
        shortest_path[node].reverse()
        parent_node = old_parent_node
        weight_queue = []

        for sort_node in children:
            weight_queue.append((sort_node, children[sort_node]['weight']))
        sorted_weights = sorted(weight_queue, key=lambda x: x[1])

        for nodes in sorted_weights:
            # If s is not in reached then
            child = nodes[0]
            cost = total_cost[parent_node] + graph.get_edge_weight(child, parent_node)
            if child not in total_cost or cost < total_cost[child]:
                if goal in total_cost and cost > total_cost[goal]:
                    pass
                else:
                    # Add child to frontier
                    if child not in shortest_path:
                        frontier.append((cost, child))
                    # we use this to solve our path
                    parent_history[child] = parent_node
                    # add child to reached
                    total_cost[child] = cost

    print(shortest_path)
    return shortest_path
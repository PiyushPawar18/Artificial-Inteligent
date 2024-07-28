def bfs_paths(graph, start, goal):
    queue = [(start, [start])]  # Queue initialized with the start node and its path
    while queue:
        (vertex, path) = queue.pop(0)  # Dequeue the first element
        for next_node in graph[vertex] - set(path):  # Explore neighbors not yet in the path
            if next_node == goal:
                yield path + [next_node]  # Yield the path if goal is reached
            else:
                queue.append((next_node, path + [next_node]))  # Enqueue the new path

# Example usage
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'C', 'E'}
}

# Generating all paths from 'A' to 'F'
paths = list(bfs_paths(graph, 'A', 'F'))
print(paths)  # Output: [['A', 'B', 'E', 'F'], ['A', 'C', 'F']]

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': []
}

def dfs_stack(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()  # LIFO
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            
            # Add neighbors in reverse to maintain order
            stack.extend(reversed(graph[node]))

# Test
dfs_stack(graph, 'A')
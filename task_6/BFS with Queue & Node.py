class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

root = Node('A')
root.left = Node('B')
root.right = Node('C')
root.left.left = Node('D')
root.left.right = Node('E')
root.right.right = Node('F')

from collections import deque

def bfs_with_queue(root):
    if not root:
        return
    
    queue = deque()
    queue.append(root)

    while queue:
        node = queue.popleft()
        print(node.value, end=" ")

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

# Test
bfs_with_queue(root)
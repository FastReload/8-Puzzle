
class Node:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth

    def __lt__(self, other):
        return self.cost < other.cost

def find_blank(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                return i, j

def expand(node):
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    blank_i, blank_j = find_blank(node.state)
    size = len(node.state)
    children = []

    for move, (di, dj) in directions.items():
        ni, nj = blank_i + di, blank_j + dj
        if 0 <= ni < size and 0 <= nj < size:
            node.state[blank_i][blank_j], node.state[ni][nj] = node.state[ni][nj], node.state[blank_i][blank_j]
            children.append(Node(node.state, parent=node, action=move, cost=node.cost + 1, depth=node.depth + 1))

    return children



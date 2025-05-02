

import heapq
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
            new_state = [row[:] for row in node.state]
            new_state[blank_i][blank_j], new_state[ni][nj] = new_state[ni][nj], new_state[blank_i][blank_j]
            children.append(Node(new_state, parent=node, action=move, cost=node.cost + 1, depth=node.depth + 1))

    return children

def goal_reached(state, goal):
    return state == goal

def misplaced_count(state, goal):
    return sum(1 for i in range(len(state)) for j in range(len(state[0]))
               if state[i][j] != 0 and state[i][j] != goal[i][j])

def manhattan_heuristic(state, goal):
    pos = {goal[i][j]: (i, j) for i in range(len(goal)) for j in range(len(goal[0]))}
    return sum(abs(pos[val][0] - i) + abs(pos[val][1] - j)
               for i in range(len(state)) for j in range(len(state[0]))
               if (val := state[i][j]) != 0)


def run_search(initial_state, heuristic, goal_state):
    start = Node(initial_state)
    queue = [(start.cost, start)]
    while queue:
        _, node = heapq.heappop(queue)
        if goal_reached(node.state, goal_state):
            return node
        for child in expand(node):
            h = heuristic(child.state, goal_state)
            child.cost = child.depth + h
            heapq.heappush(queue, (child.cost, child))



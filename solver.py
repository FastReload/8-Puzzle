

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
    x, y = find_blank(node.state)
    size = len(node.state)
    children = []
    for move, (dx, dy) in directions.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size:
            new_state = [row[:] for row in node.state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            children.append(Node(new_state, node, move, node.cost + 1, node.depth + 1))
    return children

def goal_reached(state, goal):
    return state == goal

def misplaced_count(state, goal):
    return sum(1 for i in range(len(state)) for j in range(len(state[0])) if state[i][j] != 0 and state[i][j] != goal[i][j])

def manhattan_heuristic(state, goal):
    pos = {goal[i][j]: (i, j) for i in range(len(goal)) for j in range(len(goal[0]))}
    return sum(abs(pos[val][0] - i) + abs(pos[val][1] - j)
               for i in range(len(state)) for j in range(len(state[0]))
               if (val := state[i][j]) != 0)

def run_search(initial_state, heuristic, goal_state):
    start = Node(initial_state)
    queue = [(start.cost, start)]
    explored = set()
    nodes_expanded = 0
    max_queue_size = 0
    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        _, node = heapq.heappop(queue)
        if goal_reached(node.state, goal_state):
            print("Goal state found!")
            print("Solution depth:", node.depth)
            print("Nodes expanded:", nodes_expanded)
            print("Max queue size:", max_queue_size)
            return node
        explored.add(str(node.state))
        nodes_expanded += 1
        for child in expand(node):
            if str(child.state) not in explored:
                h = heuristic(child.state, goal_state)
                child.cost = child.depth + h
                heapq.heappush(queue, (child.cost, child))

def get_solution_path(node):
    path = []
    while node:
        path.append((node.action, node.state))
        node = node.parent
    return path[::-1]

def make_default(size):
    nums = list(range(1, size * size)) + [0]
    return [nums[i * size: (i + 1) * size] for i in range(size)]

def read_puzzle(size, msg):
    print(msg)
    return [list(map(int, input("Row " + str(i + 1) + ": ").split())) for i in range(size)]

if __name__ == '__main__':
    SIZE = 3
    goal_state = make_default(SIZE)
    initial_state = read_puzzle(SIZE, "Enter initial state:")
    print("Choose algorithm:
1. UCS
2. Misplaced
3. Manhattan")
    algo = input("Your choice: ").strip()
    if algo == '1':
        heuristic = lambda s, g: 0
    elif algo == '2':
        heuristic = misplaced_count
    else:
        heuristic = manhattan_heuristic
    result = run_search(initial_state, heuristic, goal_state)
    if result:
        for move, state in get_solution_path(result):
            if move:
                print("Move:", move)
            for row in state:
                print(row)
            print()
    else:
        print("No solution found.")



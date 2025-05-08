
import heapq  # priority queue (min-heap) for selecting next best node
import time          # For measuring time taken per puzzle run
import tracemalloc   # For measuring memory usage
import json          # For saving and loading run statistics
import os            # For checking if the stats file already exists

# Define the name of the file where stats will be saved
stats_file = "stats.json"

# If the stats file already exists, load existing stats into memory
if os.path.exists(stats_file):
    with open(stats_file, "r") as f:
        stats = json.load(f)
# If the file doesn't exist, start with an empty list of stats
else:
    stats = []
# Represents a single configuration/state in the search tree
class Node:
    def __init__(self, state, parent=None, action=None, cost=0, depth=0):
        self.state = state      # current puzzle state as a 2D list
        self.parent = parent    # reference to parent node for backtracking
        self.action = action    # move taken to reach this node ('up', 'down', etc.)
        self.cost = cost        # f(n) = g(n) + h(n)
        self.depth = depth      # g(n), depth from initial node

    def __lt__(self, other):
        # Required for priority queue comparison
        return self.cost < other.cost

# Finds position of blank tile (represented by 0)
def find_blank(state):
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] == 0:
                return i, j
    raise Exception("No blank tile found!")

# Generates valid child nodes by moving the blank tile in all possible directions
def expand(node):
    moves = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }

    children = []
    size = len(node.state)
    blank_i, blank_j = find_blank(node.state)

    for move, (di, dj) in moves.items():
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < size and 0 <= new_j < size:
            new_state = [row[:] for row in node.state]  # deep copy of state
            # Swap blank with target tile
            new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
            # Create new child node with updated state
            child = Node(new_state, parent=node, action=move, cost=node.cost + 1, depth=node.depth + 1)
            children.append(child)

    return children

# Goal check: To determine if we need to go further or stop and print the result.
def goal_reached(state, goal):
    return state == goal

# Heuristic: counts number of misplaced tiles (excluding blank)
def misplaced_count(state, goal):
    cnt = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                cnt += 1
    return cnt

# Heuristic: Manhattan distance for all tiles from their goal positions
def manhattan(state, goal):
    pos = {}
    size = len(state)
    # Build lookup for goal positions
    for i in range(size):
        for j in range(size):
            pos[goal[i][j]] = (i, j)

    dist = 0
    for i in range(size):
        for j in range(size):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = pos[val]
                dist += abs(goal_i - i) + abs(goal_j - j)
    return dist

# Core search algorithm: UCS or A* depending on heuristic
def run_search(initial_state, heuristic, goal_state):
    # Create the initial node with the starting state
    start_node = Node(initial_state)

    # Priority queue (min-heap) for frontier; stores (cost, node) tuples
    frontier = []
    heapq.heappush(frontier, (start_node.cost, start_node))  # Push the initial node

    explored = set()  # To keep track of visited states (avoid revisiting)

    nodes_expanded = 0         # Counter for number of nodes expanded
    max_queue_size = 0         # Tracks maximum size of the frontier at any point

    # Begin search loop
    while frontier:
        # Update the record of the largest frontier size
        max_queue_size = max(max_queue_size, len(frontier))

        # Pop the node with the lowest f(n) = g(n) + h(n) from the queue
        _, node = heapq.heappop(frontier)


        if goal_reached(node.state, goal_state):
            print("---------------------------------------------------------------------")
            print("Goal state found!")
            print("---------------------------------------------------------------------")
            print("Solution depth:", node.depth)
            print("Nodes expanded:", nodes_expanded)
            print("Max queue size:", max_queue_size)
            return node

        explored.add(str(node.state))
        nodes_expanded += 1

        for child in expand(node):
            if str(child.state) not in explored:
                h = heuristic(child.state, goal_state)        # Estimate cost to goal
                child.cost = child.depth + h                 # f(n) = g(n) + h(n)
                heapq.heappush(frontier, (child.cost, child))  # Add to frontier

                # Print state expansion for visibility
                print("The best state to expand with g(n) =", child.depth, "and h(n) =", h, "is:")
                for row in child.state:
                    print(row)
                print()

    return None  # No solution found

# Traces back the solution path from goal to start
def solution(node):
    path = []
    while node is not None:
        path.append((node.action, node.state))
        node = node.parent
    return path[::-1]  # return reversed path

# Helper to input puzzle state row by row
def read_puzzle(size, msg):
    print(msg)
    puzzle = []
    for i in range(size):
        print("Enter row", i + 1, ":")
        row = list(map(int, input().split()))
        puzzle.append(row)
    return puzzle

# Generates default goal for 8-puzzle or 15-puzzle
def make_default(size):
    nums = list(range(1, size * size)) + [0]
    goal = []
    for i in range(size):
        goal.append(nums[i * size: (i + 1) * size])
    return goal

# Main execution flow
if __name__ == '__main__':
    SIZE = 3  # Change this to make it a 15 or higher puzzle
   # Display the puzzle header and size
print("---------------------------------------------------------------------")
print(f"Welcome to the {(SIZE**2) - 1}-Puzzle Solver!")
print("---------------------------------------------------------------------")
print("Puzzle size:", SIZE, "x", SIZE)

# Ask user whether to use default or custom goal state
print("1. Use default goal state")
print("2. Enter custom goal state")
choice = input("Your choice: ").strip()

# Set the goal state based on user input
if choice == '1':
    goal_state = make_default(SIZE)
else:
    goal_state = read_puzzle(SIZE, "Enter goal state with a space after each number:")

# Read the initial puzzle state from user
initial_state = read_puzzle(SIZE, "Enter initial state with a space after each number:")

# Prompt user to choose the search algorithm
print("Choose an algorithm to solve the puzzle:")
print("1. Uniform Cost Search")
print("2. A* with Misplaced Tile")
print("3. A* with Manhattan Distance")
algo = input("Your choice: ").strip()

# Assign the corresponding heuristic function
if algo == '1':
    heuristic = lambda s, g: 0  # UCS: no heuristic
elif algo == '2':
    heuristic = misplaced_count  # A* with misplaced tiles
else:
    heuristic = manhattan  # A* with Manhattan distance

# Display the initial board and heuristic values
print("---------------------------------------------------------------------")
print("Here’s the starting board:")
for row in initial_state:
    print(row)
h_value = heuristic(initial_state, goal_state)
print("---------------------------------------------------------------------")
print("g(n) = 0", "h(n) =", h_value, "f(n) =", h_value)
print("---------------------------------------------------------------------")

# Start measuring memory and time
tracemalloc.start()
start_time = time.time()

# Run the selected search algorithm
result = run_search(initial_state, heuristic, goal_state)

# Stop time and memory tracking
end_time = time.time()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Compute elapsed time and memory usage
elapsed_time = end_time - start_time
peak_kb = peak / 1024

# Display performance metrics
print("---------------------------------------------------------------------")
print(f"Time taken: {elapsed_time:.4f} seconds")
print(f"Peak memory used: {peak_kb:.2f} KB")
print("---------------------------------------------------------------------")

# If a solution was found, display the full path
if result:
    path = solution(result)
    print(f"Total moves: {len(path)-1}")
    for move, state in path:
        if move:
            print("Move:", move)
        for row in state:
            print(row)
        print()

    # Identify algorithm name for logging
    if algo == '1':
        algo_name = "UCS"
    elif algo == '2':
        algo_name = "A* (Misplaced Tile)"
    else:
        algo_name = "A* (Manhattan Distance)"

    # Store result for plotting/statistics
    stats.append({
    'algorithm': algo_name,
    'depth': len(path) - 1 if result else None,
    'time_sec': elapsed_time,
    'memory_kb': peak_kb
    })

    # Save the updated stats list back to file
    with open(stats_file, "w") as f:
      json.dump(stats, f, indent=4)


print("
================ Summary of Runs ================
")
for i, record in enumerate(stats, 1):
    print(f"Run {i}: Algorithm: {record['algorithm']}, Depth: {record['depth']}, Time: {record['time_sec']:.4f}s, Memory: {record['memory_kb']:.2f}KB")


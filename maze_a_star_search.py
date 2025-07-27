#This is a maze solver which I wrote to understand the concept
#of Search Algorithms and Node in artificial intelligence
#This maze solver tries to find the best path using A* search algorithm

import heapq
import itertools
maze = [
    "##########",
    "#A   #   #",
    "# ##   # #",
    "#   ##   #",
    "## #  ##B#",
    "##########"
]

start = (1, 1)
goal = (4, 8)

class Node:
     def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

def heuristic(current_state, goal_state):
    (x1, y1) = current_state
    (x2, y2) = goal_state
    return abs(x1-x2) + abs(y1-y2)

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.counter = itertools.count()
    def add(self, priority, node):
        count = next(self.counter)
        heapq.heappush(self.elements, (priority, count, node))
    def remove(self):
        return heapq.heappop(self.elements)[2]
    def is_empty(self):
        return len(self.elements)==0

def a_star_search(start, goal, maze):
    frontier = PriorityQueue()
    starting_node = Node(start, None, None, 0)
    frontier.add(0, starting_node)
    explored = set()
    while not frontier.is_empty():
        node = frontier.remove()
        if node.state == goal:
            return node
        explored.add(node.state)
        for action, (dx,dy) in [("up", (0,1)), ("down", (0,-1)), ("right", (1,0)), ("left", (-1,0))]:
            x, y = node.state[0] + dx, node.state[1] + dy
            next_states = (x, y)
            if maze[x][y] != '#' and next_states not in explored:
                cost = node.cost + 1
                h = heuristic((x, y), goal)
                total = h + cost
                child = Node(next_states, node, action, cost)
                frontier.add(total, child)
    return None

def construst_path(goal_node):
    path = []
    node = goal_node
    while node.parent is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

def showing_path(maze, path):
    maze_copy = [list(row) for row in maze]
    for r, c in path:
        if maze_copy[r][c] == " ":
            maze_copy[r][c] = "*"
    for row in maze_copy:
        print("".join(row))

solution_node = a_star_search(start, goal, maze)
path = construst_path(solution_node)
showing_path(maze, path)

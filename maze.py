class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def containState(self, node):
        return any(node.state == n.state for n in self.frontier)


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Maze():
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        # print(self.width, self.height)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        walls = self.walls
        solution = self.solution[1] if self.solution is not None else []

        print()
        for i in range(self.height):
            for j in range(self.width):
                if walls[i][j]:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif (i, j) in solution:
                    print("*", end="")
                # elif walls[i][j] == "-":
                #     print("-", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        actions = [("up", (row-1, col)), ("down", (row+1, col)),
                   ("left", (row, col-1)), ("right", (row, col+1))]
        validActions = []

        for action, (r, c) in actions:
            try:
                if not self.walls[r][c]:
                    validActions.append((action, (r, c)))
            except:
                continue

        return validActions

    def solve(self):
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        explored = set()
        num_explored = 0

        frontier.add(start)

        while True:
            if (frontier.empty()):
                raise Exception("No solution")

            node = frontier.remove()
            explored.add(node.state)
            # self.walls[node.state[0]][node.state[1]] = "-"
            num_explored += 1

            if (node.state == self.goal):
                # solution found
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                print("Number of explored nodes: ", num_explored)
                return

            for action, state in self.neighbors(node.state):
                if state not in explored and not frontier.containState(node):
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


# class main():
#     maze = Maze("maze.txt")
#     print("Maze:")
#     maze.print()
#     maze.solve()
#     print("Solution:")
#     maze.print()

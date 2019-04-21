import math

class Puzzle(object):

    def __init__(self, config, n):

        if n*n != len(config) or n < 2:
            raise Exception("Puzzle not valid!")

        self.n = n
        self.config = config
        self.children = []
        self.moves = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = int(i / self.n)
                self.blank_col = i % self.n
                self.blank_index = i
                break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            index = self.blank_index
            target = index - 1
            new_config = list(self.config)
            new_config[index], new_config[target] = new_config[target], new_config[index]
            return tuple(new_config)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            index = self.blank_index
            target = index + 1
            new_config = list(self.config)
            new_config[index], new_config[target] = new_config[target], new_config[index]
            return tuple(new_config)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            index = self.blank_index
            target = index - self.n
            new_config = list(self.config)
            new_config[index], new_config[target] = new_config[target], new_config[index]
            return tuple(new_config)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            index = self.blank_index
            target = index + self.n
            new_config = list(self.config)
            new_config[index], new_config[target] = new_config[target], new_config[index]
            return tuple(new_config)

    def expand(self):
        # Add child nodes in order UDLR (Up,Down,Left,Right)
        if len(self.children) == 0:
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child) 
                self.moves.append('Up') 
            down_child = self.move_down()
            if down_child is not None:
                self.children.append(down_child)
                self.moves.append('Down')
            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)
                self.moves.append('Left')
            right_child = self.move_right()
            if right_child is not None:
                self.children.append(right_child)
                self.moves.append('Right')
        return self.children,self.moves

def solution(dictionary,goal,initial_state):

    moves = []
    while goal != initial_state:
        for key,value in dictionary.items():
            if key == goal:
                moves.append(value[1])
                goal = value[0]
                break

    moves.reverse()
    cost = len(moves)
    return moves,cost

def bfs_search(begin_state,goal):

    size = int(math.sqrt(len(begin_state)))
    initial_state = Puzzle(begin_state,size)

    print("Solving Puzzle...")
    initial_state.display()
    
    frontier = [initial_state.config]
    explored = []
    dictionary = {}

    while not frontier == []:
        state = frontier[0]
        frontier.remove(frontier[0])
        explored.append(state)
        PuzzleState = Puzzle(state,size)

        if goal == state:
            print("Solved!")
            PuzzleState.display()
            moves,cost = solution(dictionary,goal,initial_state.config)
            return ("Cost: {} - Solution: {}".format(cost,moves))

        children,moves = PuzzleState.expand()
        for index in range(0,len(children)):
            child = children[index]
            move = moves[index]
            if not (child in frontier or child in explored):
                frontier.append(child)
                dictionary[child] = (PuzzleState.config,move)

    return "No Solution Found"
    

if __name__ == '__main__':

    begin_state = tuple([0,1,2,4,5,3,7,8,6]) 
    goal = tuple([1,2,3,4,5,6,7,8,0])
    print(bfs_search(begin_state,goal))

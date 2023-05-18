class State:
    def __init__(self, state, parent, depth, move, currPlayer):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.move = move
        self.currPlayer = currPlayer
    
    def printState(self):
        print('| {} {} {} |\n| {} {} {} |\n| {} {} {} |\n'.format(self.state[0], self.state[1], 
        self.state[2], self.state[3], self.state[4], self.state[5], self.state[6], self.state[7], self.state[8]))
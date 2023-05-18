from state import *
import random as r

maxPlayer, minPlayer = 'X', 'O'
bestScore = 0

# Tkinter functions
def update_state(curr, r, c, v):
    curr[r * 3 + c] = get_symbol(v)
    return not v


def get_symbol(v):
    return 'X' if v else 'O'


def gen_moves(curr, v):
    s = get_symbol(v)
    poss_moves = []
    for i, x in enumerate(curr):
        if x == -1:
            poss_moves.append(curr[:])
            poss_moves[-1][i] = s
    r.shuffle(poss_moves)
    return poss_moves


def is_won(curr: list):
    for i in range(3):
        if curr[3 * i + 0] == curr[3 * i + 1] == curr[3 * i + 2] != -1: return True
        if curr[0 + i] == curr[3 + i] == curr[6 + i] != -1: return True
    return curr[0] == curr[4] == curr[8] != -1 or curr[2] == curr[4] == curr[6] != -1


def is_draw(curr: list):
    return -1 not in curr


def final_score(curr):
    res = 0
    for x in curr:
        if x == -1: res += 1
    return res


def find_best_move(curr, is_ai, v):
    if is_won(curr): return curr, 1 + final_score(curr) if not is_ai else -final_score(curr) - 1  # invert the flag
    if is_draw(curr): return curr, 0
    poss_moves = gen_moves(curr, v)
    b = -10 if is_ai else 10
    next_move = None
    for move in poss_moves:
        _, score = find_best_move(move, not is_ai, not v)
        if (score > b and is_ai) or (score < b and not is_ai):
            next_move, b = move, score
    return next_move, b

# Raw Code functions
def isGameOver(state):
    '''
    Will check whether the game is over, returns true if it's over.
    '''
    for i in range(9):
        if state.state[i] == '_':
            break
        if i == 8:
            return True;

    # check horizontal win
    for i in (0, 3, 6):
        if (state.state[i] == maxPlayer and state.state[i+1] == maxPlayer 
            and state.state[i+2] == maxPlayer) or (state.state[i] == minPlayer and 
        state.state[i+1] == minPlayer and state.state[i+2] == minPlayer):
            return True 
    
    # check vertical win
    for i in range(3):
        if (state.state[i] == 'O' and state.state[i+3] == 'O' and state.state[i+6] == 'O') or (state.state[i] == 'X' and 
            state.state[i+3] == 'X' and state.state[i+6] == 'X'):
            return True
    
    # check diagonal win
    if ((state.state[0] == 'O' and state.state[4] == 'O' and state.state[8] == 'O') or (state.state[2] == 'O' 
        and state.state[4] == 'O' and state.state[6] == 'O') or (state.state[0] == 'X' and state.state[4] == 'X' 
        and state.state[8] == 'X') or (state.state[2] == 'X' and state.state[4] == 'X' and state.state[6] == 'X')):
        return True

    # if this triggers then no one has won yet
    return False

def evalFunc(state):
    '''
    Will check the current state of the board. Returns 0 if draw or not finished, 10 if max win, and
    -10 if min win.
    '''

    # check horizontal win
    for i in (0, 3, 6):
        if (state.state[i] == maxPlayer and state.state[i+1] == maxPlayer and state.state[i+2] == maxPlayer):
            return 100 - state.depth
        elif(state.state[i] == minPlayer and state.state[i+1] == minPlayer and state.state[i+2] == minPlayer):
            return -100 + state.depth
    
    # check vertical win
    for i in range(3):
        if (state.state[i] == 'O' and state.state[i+3] == 'O' and state.state[i+6] == 'O'):
            return -100 + state.depth
        elif(state.state[i] == 'X' and state.state[i+3] == 'X' and state.state[i+6] == 'X'):
            return 100 - state.depth
    
    # check diagonal win
    if ((state.state[0] == 'O' and state.state[4] == 'O' and state.state[8] == 'O') or 
        (state.state[2] == 'O' and state.state[4] == 'O' and state.state[6] == 'O')):
        return -100 + state.depth
    elif((state.state[0] == 'X' and state.state[4] == 'X' and state.state[8] == 'X') or 
         (state.state[2] == 'X' and state.state[4] == 'X' and state.state[6] == 'X')):
        return 100 - state.depth

    # check for full board
    for i in range(9):
        if state.state[i] == '_':
            break
        if i == 8:
            return 0;

    # if this triggers then no one has won yet
    return 0


def minimax(nextState):
    '''
    Returns the evaluation value of the node if it's the leaf node.
    Or will recursively call itself to it's child node.
    '''
    score = evalFunc(nextState)
    # print('MINIMAX:::::')
    # print('For this state')
    # nextState.printState()
    # print('this is what ' + str(nextState.currPlayer))
    # print(
    #     'This is evalfunc', str(score) + '\n\n\n\n\n'
    # )
    # Return score if reached terminal state
    if score != 0:
        return score

    # Checks if there are any moves left
    for i in range(9):
        if nextState.state[i] == '_':
            break
        if i == 8:
            return 0
    
    if nextState.currPlayer == 'O':
        bestVal = 100
        for i in range(9):
            if nextState.state[i] == '_':
                nextState.state[i] = 'O'
                bestVal = min(bestVal, minimax(State(nextState.state, nextState, nextState.depth+1, None, maxPlayer)))
                nextState.state[i] = '_'
        return bestVal
    else:
        bestVal = -100
        for i in range(9):
            if nextState.state[i] == '_':
                nextState.state[i] = 'X'
                bestVal = max(bestVal, minimax(State(nextState.state, nextState, nextState.depth+1, None, minPlayer)))
                nextState.state[i] = '_'
        return bestVal

def findBestMove(state):
    '''
    Gets the input of a state of the game and returns a tuple
    of the best move state and it's score
    '''

    if state == -1:
        print('Invalid state')
        exit()

    nextState = State(state.state, state, state.depth+1, None, None)

    if state.currPlayer == 'X':
        bestVal = -1000
        nextState.currPlayer = 'O'
    else:
        bestVal = 1000
        nextState.currPlayer = 'X'

    bestStateIndex = -1
    for i in range(9):
        if nextState.state[i] == '_':
            nextState.state[i] = state.currPlayer

            newMoveVal = minimax(nextState)
            # print('this is newmoveval For' + str(newMoveVal) + '\n')
            # nextState.printState()
            # print(newMoveVal)
            nextState.state[i] = '_'
            if state.currPlayer == 'X' and newMoveVal > bestVal:
                bestVal = newMoveVal
                bestStateIndex = i

            elif state.currPlayer == 'O' and newMoveVal < bestVal:
                bestVal = newMoveVal
                bestStateIndex = i
    if bestStateIndex != -1:
        nextState.state[bestStateIndex] = state.currPlayer

    # print("Break\n\n\n\n")
    return nextState;

def enterInIndex(state, index):
    if index > 8 or index < 0 or state.state[index] != '_':
        print('Please enter a valid index')
        return -1

    if state.currPlayer == 'X':
        newState = State(state.state, state, state.depth + 1, None, minPlayer)
        newState.state[index] = state.currPlayer
    else:
        newState = State(state.state, state, state.depth + 1, None, maxPlayer)
        newState.state[index] = state.currPlayer

    return newState
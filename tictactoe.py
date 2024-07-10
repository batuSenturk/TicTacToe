"""
Tic Tac Toe Player
"""
import copy
import math
import random

X = "X"
O = "O"
EMPTY = None

CORNERS = [(0, 0), (0, 2), (2, 0), (2, 2)]

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def piece_count(p, board):
    """
    Counts the number of occurances of a piece on the board at a given time.
    """
    return sum(row.count(p) for row in board)


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = piece_count(X, board)
    o_count = piece_count(O, board)
    #since X goes first, it will either be that X and O will have the same number of occurances or X will have one more
    if x_count == o_count:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    #scan every node
    for i in range(3):
        for j in range(3):
            #if the node does not have a set value, add it to the set of actions
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    if i < 0 or i >= 3 or j < 0 or j >= 3:
        raise ValueError("Action is out of bounds")

    if board[i][j] == X or board[i][j] == O:
        raise ValueError("Cell has a value")
    
    updated_board = copy.deepcopy(board)
    updated_board[i][j] = player(board)
    return updated_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #rows and columns check
    for i in range(3):
        if board[i][0] is not EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] is not EMPTY and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
        
    #check diagonals
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[1][1] is not EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    #this does not seem right but I was recommended in a section to hard-code the algorithm so that its first choice is one of the corners
    flag = True
    if player(board) == X:
        for row in board:
            for cell in row:
                if cell is not EMPTY:
                    flag = False
        if flag:
            return random.choice(CORNERS)

    #recursive technique for the implementation of the base of minimax
    #seemed perfect for recursive
    def max_value(board):
        if terminal(board):
            return utility(board)
        var = -math.inf
        for a in actions(board):
            var = max(var, min_value(result(board, a)))
        return var
    
    def min_value(board):
        if terminal(board):
            return utility(board)
        var = math.inf
        for a in actions(board):
            var = min(var, max_value(result(board, a)))
        return var
    
    #calculate in each case and update the best move
    if player(board) == X:
        best_val = -math.inf
        best_a = None
        for a in actions(board):
            val = min_value(result(board, a))
            if val > best_val:
                best_val = val
                best_a = a
            
    else:
        best_val = math.inf
        best_a = None
        for a in actions(board):
            val = max_value(result(board, a))
            if val < best_val:
                best_val = val
                best_a = a

    return best_a
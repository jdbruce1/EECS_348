import struct, string

class TicTacToeBoard:

    def __init__(self):
        self.board = (['N']*3,['N']*3,['N']*3)
                                      
    def PrintBoard(self):
        print(self.board[0][0] + "|" + self.board[1][0] + "|" + self.board[2][0])
        
        print(self.board[0][1] + "|" + self.board[1][1] + "|" + self.board[2][1])
        
        print(self.board[0][2] + "|" + self.board[1][2] + "|" + self.board[2][2])
        
    def play_square(self, col, row, val):
        self.board[col][row] = val

    def get_square(self, col, row):
        return self.board[col][row]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j]=='N'):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return 'N'
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!='N' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
        #check the rows
        for row in range(3):
            if(self.board[0][row]!='N' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]
        #check diagonals
        if(self.board[0][0]!='N' and self.board[0][0] == self.board[1][1] and self.board[0][0]==self.board[2][2] ):
            return self.board[0][0]
        if(self.board[2][0]!='N' and self.board[2][0] == self.board[1][1] and self.board[2][0]==self.board[0][2]):
            return self.board[2][0]
        return 'N'

def make_simple_cpu_move(board, cpuval):
    for i in range(3):
        for j in range(3):
            if(board.get_square(i,j)=='N'):
                board.play_square(i,j,cpuval)
                return True
    return False

def actions(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board.get_square(i, j) == 'N':
                moves.append({"row":i,"col":j})
    return moves

def utility(board, cpuval):
    winner = board.winner()
    if winner == 'N':
        if not board.full_board():
            print "Utility function called on an unfilled board."
        return 0
    elif winner == cpuval:
        return 1
    else:
        return -1

def terminal_test(board):
    if board.full_board():
        return True
    else:
        w = board.winner()
        if w == 'N':
            return False
        return True

def result(board, action, cpuval):
    new_board = TicTacToeBoard()
    for i in range(3):
        for j in range(3):
            new_board.play_square(i, j, board.get_square(i, j))
            new_board.play_square(action["row"], action["col"], cpuval)
    return new_board

def max_value(board,cpuval, playerval, alpha, beta):
    if(terminal_test(board)):
        return utility(board,cpuval)
    v = -2
    for a in actions(board):
        v = max(v,min_value(result(board,a,cpuval),cpuval, playerval,alpha,beta))
        a["value"] = v
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(board,cpuval, playerval, alpha, beta):
    if(terminal_test(board)):
        return utility(board,cpuval)
    v = 2
    for a in actions(board):
        v = min(v,max_value(result(board,a,playerval),cpuval, playerval, alpha, beta))
        a["value"] = v
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def minimax_decision(board, cpuval, playerval):
    best_action = None
    best_value = -2
    list_of_actions = actions(board)

    if not list_of_actions:
        return False
    v = max_value(board,cpuval,playerval,-2,2);

    for action in list_of_actions:
        value = min_value(result(board, action, cpuval), cpuval, playerval,-2,2)
        if value == v:
            board.play_square(action["row"], action["col"], cpuval)
            return True

def play():
    Board = TicTacToeBoard()
    humanval =  'X'
    cpuval = 'O'
    Board.PrintBoard()
    
    while( Board.full_board()==False and Board.winner() == 'N'):
        print("your move, pick a row (0-2)")
        row = int(input())
        print("your move, pick a col (0-2)")
        col = int(input())

        if(Board.get_square(col,row)!='N'):
            print("square already taken!")
            continue
        else:
            Board.play_square(col,row,humanval)
            if(Board.full_board() or Board.winner()!='N'):
                break
            else:
                Board.PrintBoard()
                print("CPU Move")
                minimax_decision(Board,cpuval, humanval)
                Board.PrintBoard()

    Board.PrintBoard()
    if(Board.winner()=='N'):
        print("Cat game")
    elif(Board.winner()==humanval):
        print("You Win!")
    elif(Board.winner()==cpuval):
        print("CPU Wins!")

def main():
    board = TicTacToeBoard()
    humanval = 'X'
    cpuval = 'O'
    # board.PrintBoard()
    # # print "-------"
    # # new_board = result(board, {"row":0, "col": 2}, 'O')
    # # print "old board"
    # # board.Printboard()
    # # print "new board"
    # # new_board.Printboard()

    # board.play_square(0, 0, 'X')
    # board.play_square(1, 0, 'O')
    # board.play_square(0, 1, 'X')
    # board.play_square(2, 1, 'O')
    # board.play_square(0, 2, 'O')
    # board.play_square(1, 2, 'X')
    # board.play_square(2, 2, 'O')
    # board.PrintBoard()
    # minimax_decision(board, 'O', 'X')
    # board.PrintBoard()
    # print max_value(board, 'O')
    # board.Printboard()
    # print actions(board)
    # print utility(board, 'O')
    # print terminal_test(board)
    play()



main()






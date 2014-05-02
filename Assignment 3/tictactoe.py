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

def result(board, action):
    new_board = TicTacToeBoard()
    for i in range(3):
        for j in range(3):
            new_board[i][j] = board[i][j]
    board.play_square(action["row"], action["col"])
    return new_board


# def minimax_decision(board, cpuval):

# def max_value(board, assignments)




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
                make_simple_cpu_move(Board,cpuval)
                Board.PrintBoard()

    Board.PrintBoard()
    if(Board.winner()=='N'):
        print("Cat game")
    elif(Board.winner()==humanval):
        print("You Win!")
    elif(Board.winner()==cpuval):
        print("CPU Wins!")

def main():
    Board = TicTacToeBoard()
    humanval = 'X'
    cpuval = 'O'
    Board.PrintBoard()
    print "-------"
    Board.play_square(0, 0, 'X')
    Board.play_square(1, 0, 'O')
    Board.play_square(2, 0, 'X')
    Board.play_square(0, 1, 'O')
    Board.play_square(1, 1, 'X')
    Board.play_square(2, 1, 'O')
    Board.play_square(0, 2, 'X')
    Board.play_square(1, 2, 'X')
    Board.play_square(2, 2, 'O')
    Board.PrintBoard()
    # print actions(Board)
    # print utility(Board, 'O')
    print terminal_test(Board)
    # play()



main()






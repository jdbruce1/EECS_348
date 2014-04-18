#!/usr/bin/env python
import struct, string, math

#this will be the game object your player will manipulate
class SudokuBoard:

    #the constructor for the SudokuBoard
    def __init__(self, size, board):
      self.BoardSize = size #the size of the board
      self.CurrentGameboard= board #the current state of the game board

    #This function will create a new sudoku board object with
    #with the input value placed on the GameBoard row and col are
    #both zero-indexed
    def set_value(self, row, col, value):
        self.CurrentGameboard[row][col]=value #add the value to the appropriate position on the board
        return SudokuBoard(self.BoardSize, self.CurrentGameboard) #return a new board of the same size with the value added
    
    def print_board(self):
        for row in range(self.BoardSize):
            row_out = ""
            for col in range(self.BoardSize):
                row_out = row_out + str(self.CurrentGameboard[row][col]) + " "
            print row_out


# parse_file
#this function will parse a sudoku text file (like those posted on the website)
#into a BoardSize, and a 2d array [row,col] which holds the value of each cell.
# array elements witha value of 0 are considered to be empty

def parse_file(filename):
    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    



#takes in an array representing a sudoku board and tests to
#see if it has been filled in correctly
def iscomplete( BoardArray ):
        size = len(BoardArray)
        subsquare = int(math.sqrt(size))

        #check each cell on the board for a 0, or if the value of the cell
        #is present elsewhere within the same row, column, or square
        for row in range(size):
            for col in range(size):

                if BoardArray[row][col]==0:
                    return False
                for i in range(size):
                    if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                        return False
                    if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                        return False
                #determine which square the cell is in
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        if((BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == BoardArray[row][col])
                           and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                            return False
        return True

# creates a SudokuBoard object initialized with values from a text file like those found on the course website
def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

# consistent Function
def consistent(assignment, row, col, val):
# check to see if tuple is consistent with assignment

def select_unassigned_variable(board):
    for r in range(board.BoardSize):
        for c in range(board.BoardSize):
            if board.CurrentGameboard[r][c] == 0:
                return r, c

def in_domain(row,col,val,board):
    # row check
    for r in range(board.BoardSize)):
        if board.CurrentGameboard[r][col] == val:
            return False
    # column check
    for c in range(board.BoardSize)):
        if board.CurrentGameboard[row][c] == val:
            return FTrue
    # subsquare check
    subsquare = int(math.sqrt(board.BoardSize)))
    squareRow = row // subsquare
    squareCol = col // subsquare
    
    for r in range(subsquare):
        for c in range(subsquare):
            if board.CurrentGameboard[squareRow * subsquare + r][squareCol * subsquare + c] == val:
                return False
    return True

def order_domain_values(row,col,assignment,board):
    domain_values = []
    for x in range(1,board.BoardSize):
        if in_domain(row,col,x,board):
            domain_values.append(x)
    return domain_values


    # numbers = []
    # for x in range(1,board.BoardSize+1):
    #     numbers.append(x);
    # return numbers





def backtrack(assignment, board):
    if iscomplete(assignment):
        return assignment
    row, col = select_unassigned_variable(board)
    for val in order_domain_values(row, col, assignment, board):
        if consistent(assignment, row, col, val):
            assignment.append = [row,col,val]
            result = backtrack(assignment, board)
            if result != None:
                return result
        assignment.pop()
    return None








# Test code to print a board for debugging
test_board = parse_file('test1.txt')
tboard = SudokuBoard(len(test_board),test_board)
tboard.print_board()

# consistent test cases for test1.text when line 2 = 3. Tests subsquares
# print consistent(tboard, 1,0,2)
# print consistent(tboard, 0,0,2)
# print consistent(tboard, 1,1,2)
# print consistent(tboard, 3,0,3)

# order_domain_values test
# print order_domain_values(0,0,0,tboard)

# consistent test cases for test1.txt
# print consistent(tboard, 2, 0, 4)
# print consistent(tboard, 0, 0, 2)
# print consistent(tboard, 0, 1, 2)
# print consistent(tboard, 0, 2, 4)
# print consistent(tboard, 0, 0, 1)
























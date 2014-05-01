import EECS_348_Sudoku as sudoku
import math

variable_assignment_count = {0:0}

def select_unassigned_variable(board,assignment):
    for r in range(board.BoardSize):
        for c in range(board.BoardSize):
            if not sudoku.is_assigned(r,c,board,assignment):
                return r, c

def backtrack_forward(assignment, board, domains, variable_assignment_count):
    variable_assignment_count[0] = variable_assignment_count[0] + 1
    # Tests for completion by adding assignments to board, then restores if not
    for i in range(len(assignment)):
        board.CurrentGameboard[assignment[i][0]][assignment[i][1]] = assignment[i][2]
    #board.print_board()
    if sudoku.iscomplete(board.CurrentGameboard):
        return assignment
    for i in range(len(assignment)):
        board.CurrentGameboard[assignment[i][0]][assignment[i][1]] = 0
    # Selects the variable to try values for
    row, col = select_unassigned_variable(board,assignment)
    # Tries each possible value in the variable's domain
    for val in sudoku.odv_forward(row,col,domains):
        if sudoku.consistent(assignment, row, col, val,board.BoardSize):   # If that value works, adds it to the assignment
            assignment.append([row,col,val])
            domains, changes, possible = sudoku.forward_check(row,col,val,domains,board,assignment) # Also, restricts the domain of other variables
            if possible: # If no conflict is immediately detected, continues to the next variable to be assigned
                result = backtrack_forward(assignment,board,domains, variable_assignment_count) 
                if result != None: # If that was successful, return its result
                    return result
            if assignment: # Otherwise, remove the assignment and restore the domains
                assignment.pop()
                domains = sudoku.reverse_forward(changes,domains)
    return None # If none of them work, return none

def backtracking_search_forward_checking(csp):
    domains = sudoku.initialize_domains(csp)
    return backtrack_forward([],csp,domains, variable_assignment_count)

# Test code for a file with a board
test_board = sudoku.parse_file('test16.txt')
tboard = sudoku.SudokuBoard(len(test_board),test_board)
tboard.print_board()

backtracking_search_forward_checking(tboard)
tboard.print_board()

print variable_assignment_count[0]
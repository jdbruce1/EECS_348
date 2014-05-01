import EECS_348_Sudoku as sudoku

variable_assignment_count = {0:0}

def order_domain_values(row,col,assignment,board):
    domain_values = []
    for x in range(1,board.BoardSize+1):
        if sudoku.in_domain(row,col,x,board):
            domain_values.append(x)
    return domain_values

def backtrack(assignment, board, variable_assignment_count):
	variable_assignment_count[0] = variable_assignment_count[0] + 1
	for i in range(len(assignment)):
		board.CurrentGameboard[assignment[i][0]][assignment[i][1]] = assignment[i][2]    
	if sudoku.iscomplete(board.CurrentGameboard):
		return assignment
	for i in range(len(assignment)):
		board.CurrentGameboard[assignment[i][0]][assignment[i][1]] = 0
	row, col = sudoku.select_unassigned_variable(board,assignment)
	for val in order_domain_values(row, col, assignment, board):
		if sudoku.consistent(assignment, row, col, val,board.BoardSize):
			assignment.append([row,col,val])
			result = backtrack(assignment, board, variable_assignment_count)
			if result != None:
				return result
			if assignment:
				assignment.pop()
	return None

def backtracking_search(csp):
    return backtrack([],csp, variable_assignment_count)

# Test code for a file with a board
test_board = sudoku.parse_file('test9.txt')
tboard = sudoku.SudokuBoard(len(test_board),test_board)
tboard.print_board()

backtracking_search(tboard)
tboard.print_board()

print variable_assignment_count[0]
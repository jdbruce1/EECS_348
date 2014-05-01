import EECS_348_Sudoku as sudoku
import math, operator

variable_assignment_count = {0:0}

def backtrack_forward_mrv_mcv_lcv(assignment, board, domains, variable_assignment_count):
    variable_assignment_count[0] = variable_assignment_count[0] + 1
    # Tests for completion by adding assignments to board, then restores if not
    # print " -------------------------"
    for i in range(len(assignment)):
        board.CurrentGameboard[assignment[i][0]][assignment[i][1]] = assignment[i][2]
    # board.print_board()
    if sudoku.iscomplete(board.CurrentGameboard):
        return assignment
    for i in range(len(assignment)):
        board.CurrentGameboard[assignment[i][0]][assignment[i][1]] = 0
    # Selects the variable to try values for
    row, col = select_unassigned_variable_mrv_mcv_lcv(board,assignment, domains)
    # Tries each possible value in the variable's domain
    for val in odv_forward_mrv_mcv_lcv(row,col,domains,board,assignment):
        if sudoku.consistent(assignment, row, col, val,board.BoardSize):   # If that value works, adds it to the assignment
            assignment.append([row,col,val])
            domains, changes, possible = sudoku.forward_check(row,col,val,domains,board,assignment) # Also, restricts the domain of other variables
            if possible: # If no conflict is immediately detected, continues to the next variable to be assigned
                result = backtrack_forward_mrv_mcv_lcv(assignment,board,domains,variable_assignment_count) 
                if result != None: # If that was successful, return its result
                    return result
            if assignment: # Otherwise, remove the assignment and restore the domains
                assignment.pop()
                domains = sudoku.reverse_forward(changes,domains)
    return None # If none of them work, return none

def backtracking_search_forward_checking_mrv_mcv_lcv(csp):
    domains = sudoku.initialize_domains(csp)
    return backtrack_forward_mrv_mcv_lcv([],csp,domains,variable_assignment_count)

def select_unassigned_variable_mrv_mcv_lcv(board,assignment,domains):
    min_row = 0
    min_col = 0
    min_len = len(board.CurrentGameboard) + 1
    constraining_val = 0

    mrv = []

    for r in range(board.BoardSize):
        for c in range(board.BoardSize):
            if not sudoku.is_assigned(r,c,board,assignment):
                key = str([r, c])
                if len(domains[key]) < min_len:
                    # val = constraining_value(r, c, board, assignment)
                    # if(val >= constraining_val):
                    min_len = len(domains[key])
                    min_row = r
                    min_col = c
                        # constraining_val = val
                elif len(domains[key]) == min_len:
                    val = constraining_value(r, c, board, assignment)
                    if(val > constraining_val):
                        min_len = len(domains[key])
                        min_row = r
                        min_col = c
                        constraining_val = val
    return min_row, min_col

def constraining_value(row, col, board, assignment):
    count = 0;
    for i in range(board.BoardSize):
        if not sudoku.is_assigned(row, i, board, assignment):
            count += 1
        if not sudoku.is_assigned(i, col, board, assignment):
            count += 1
        # print count

    subsquare = int(math.sqrt(board.BoardSize))
    squareRow = row // subsquare
    squareCol = col // subsquare
    # return count  
    for r in range(subsquare):
        for c in range(subsquare):
            if not sudoku.is_assigned(r, c, board, assignment):
                count += 1
        # print count
        return count

def odv_forward_mrv_mcv_lcv(row,col,domains,board, assignment):
    max_count = 0
    max_index = 0
    domain = domains[str([row,col])]
    dictionary = {}
    for i in range(len(domain)):
        val = domain[i]
        count = 0
        # row checking
        for r in range(board.BoardSize):
            if (not sudoku.is_assigned(r,col,board,assignment)) and domains[str([r,col])].count(val):
                count += 1
        # column checking
        for c in range(board.BoardSize):
            if (not sudoku.is_assigned(row,c,board,assignment)) and domains[str([row,c])].count(val):
                count += 1
        # subsquare checking
        subsquare = int(math.sqrt(board.BoardSize))
        squareRow = row // subsquare
        squareCol = col // subsquare
        
        for r in range(subsquare):
            for c in range(subsquare):
                if (not sudoku.is_assigned(squareRow * subsquare + r,squareCol * subsquare + c,board,assignment)) and domains[str([squareRow * subsquare + r,squareCol * subsquare + c])].count(val):
                    count += 1
        dictionary[val] = count

    sorted_dictionary = sorted(dictionary.iteritems(), key=operator.itemgetter(1))

    dom = []
    for dom_val in sorted_dictionary:
        dom.append(dom_val[0])
    return reversed(dom)
    
# Test code for a file with a board
test_board = sudoku.parse_file('test25.txt')
tboard = sudoku.SudokuBoard(len(test_board),test_board)
tboard.print_board()

backtracking_search_forward_checking_mrv_mcv_lcv(tboard)
tboard.print_board()

print variable_assignment_count[0]
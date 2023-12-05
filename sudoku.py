#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    start_time = time.time()
    constraints = initializeConstraints()
    domains = initializeDomains(board, constraints)
    board = backtrack(board, domains, constraints)
    # solved_board = board
    end_time = time.time()
    return board

"""

"""
def backtrack(board, domains, constraints):
    if completeBoard(board):
        return board
    next_pos = nextUnassigned(domains)
    # print ("next_pos", next_pos)
    for value in traverseOrder(next_pos, domains, constraints):
        if isValid(next_pos, value, board, constraints):
            board[next_pos] = value
            old_domains = deepCopy(domains)
            inferences = forwardCheck(board, domains, constraints[next_pos], value)
            if inferences is not None and inferences != False:
                inferences.pop(next_pos)
                domains = inferences.copy()
                result = backtrack(board, domains, constraints)
                if result:
                    return result
            board[next_pos] = 0
            domains = deepCopy(old_domains)
    return False

"""
initializeDomains(board, constraints): creates a dictionary of the initial domains for each UNASSIGNED space on the board
"""
def initializeDomains(board, constraints):
    domains = {}
    for r in ROW:
        for c in COL:
            if board[r + c] == 0:
                domains[r + c] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                for constraint in constraints[r + c]:
                    # print (constraint, ",", board[constraint], ",", r + c, ",", domains[r + c])
                    if board[constraint] in domains[r + c]:
                        # discard the constraint's value from the current domain (if 'A1' is assigned to 2 and 'A2's domain contains 2, take 2 out of the domain.)
                        domains[r + c].discard(board[constraint])
    return domains

""" 
initializeConstraints(board): creates a dictionary of the constraints of each space on the board (ex. {'A1': ('A2', 'A3',..., 'A9', 'B1', 'C1', ..., 'I1', 'B2', 'B3', 'C2', 'C3'}) 
"""
def initializeConstraints():
    constraints = {}
    for r in ROW:
        for c in COL:
            curr = set()

            # adding the entire row (changing c, number)
            for c1 in COL:
                if (c1 == c):
                    continue
                else:
                    curr.add(r + c1)

            # adding the entire column (changing r, letter)
            for r1 in ROW:
                if (r1 == r):
                    continue
                else:
                    curr.add(r1 + c)

            # adding the subgroup (square), will have 4 duplicates every time but b/c set, it's okay
            ROW1 = set(ROW[:3])
            ROW2 = set(ROW[3:6])
            ROW3 = set(ROW[6:])
            COL1 = set(COL[:3])
            COL2 = set(COL[3:6])
            COL3 = set(COL[6:])
            if (r in ROW1) and (c in COL1):
                for r1 in ROW1:
                    for c1 in COL1:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW1) and (c in COL2):
                for r1 in ROW1:
                    for c1 in COL2:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW1) and (c in COL3):
                for r1 in ROW1:
                    for c1 in COL3:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW2) and (c in COL1):
                for r1 in ROW2:
                    for c1 in COL1:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW2) and (c in COL2):
                for r1 in ROW2:
                    for c1 in COL2:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW2) and (c in COL3):
                for r1 in ROW2:
                    for c1 in COL3:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW3) and (c in COL1):
                for r1 in ROW3:
                    for c1 in COL1:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW3) and (c in COL2):
                for r1 in ROW3:
                    for c1 in COL2:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            elif (r in ROW3) and (c in COL3):
                for r1 in ROW3:
                    for c1 in COL3:
                        if r1 == r and c1 == c:
                            continue
                        else:
                            curr.add(r1 + c1)
            constraints[r + c] = curr
    return constraints

"""
nextUnassigned(board, domains): returns a board location in the form standardized 'A4' form
"""
def nextUnassigned(domains):
    mrv = 10
    tile = 0
    for loc in domains:
        if len(domains[loc]) < mrv:
            # print (loc, domains[loc])
            mrv = len(domains[loc])
            tile = loc
    return tile

"""
traverseOrder(domain, domains, constraints): takes a domain (set) of the next value (determined by nextUnassigned) and returns a list in the order that the domain should be visited in (in accordance with LCV - Least Constraining Value)
"""
def traverseOrder(next_pos, domains, constraints):
    d = {}
    returns = []
    for val in domains[next_pos]:
        constrains = 0
        for constraint in constraints[next_pos]:
            if constraint in domains and val in domains[constraint]:
                constrains += 1
        d[val] = constrains
    # print ("dictionary of how constraining", next_pos, "is", d)
    while len(d) != 0:
        min = 27
        minVal = 0
        for val in d:
            if d[val] < min:
                min = d[val]
                minVal = val
        returns.append(minVal)
        d.pop(minVal)
    # print ("order of checking:", returns)
    return returns

"""
isValid(position, value, board, constraints): returns a boolean on whether value at position does not violate any of the constraints according to already assigned positions
"""
def isValid(position, value, board, constraints):
    for constraint in constraints[position]:
        if value == board[constraint]:
            return False
    return True

"""
forwardCheck(domains, position, value): returns an updated domains dictionary, returns False on failure
"""
def forwardCheck(board, domains, constraint, value):
    # iterate through the tiles that position is constrained to
    for tile in constraint:
        if tile not in domains:
            if value == board[tile]:
                return False
            continue
        if value in domains[tile]:
            domains[tile].discard(value)
            if len(domains[tile]) == 0:
                return False
    return domains

"""
completeBoard(board): returns a boolean of whether there are any unassigned spaces in the board
"""
def completeBoard(board):
    vals = set(board.values())
    # print (vals)
    if 0 in vals:
        return False
    else:
        return True

def deepCopy(domains):
    new = {}
    for domain in domains:
        new[domain] = domains[domain].copy()
    return new

# def debugPrint(board, domains, )
if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = {ROW[r] + COL[c]: int(sys.argv[1][9 * r + c])
                 for r in range(9) for c in range(9)}
        start_time = time.time()
        solved_board = backtracking(board)
        end_time = time.time()

        print (end_time-start_time)
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = {ROW[r] + COL[c]: int(line[9 * r + c])
                     for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            # print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)

            # Print solved board. TODO: Comment this out when timing runs.
            # print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
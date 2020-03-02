# Created on 18 Feb 2020
# Created by: Matthew Lourenco
# This is a program that simulates sudoku
#
# Rules:
# https://sudoku.com/how-to-play/sudoku-rules-for-complete-beginners/
#
# Sample board:
'''
[[0, 0, 0, 0, 0, 1, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 6, 0, 0, 0],
 [0, 0, 0, 4, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 8, 0, 0, 0, 0],
 [2, 0, 9, 0, 0, 0, 0, 0, 7],
 [0, 0, 0, 0, 0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 3, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 0, 0]]
'''

from numpy import array


# Inputs: (int) row, (int) column, (int) value
# Outputs: Boolean
# Returns true if the number 'value' can be played at given row and column. Returns false if the number 'value' cannot
#   be placed the given row and column
def valid_play(row, col, value):

    # Check for existing number
    if board[row][col] != 0:
        return False

    # Check for valid bounds
    if row < 0 or col < 0 or value < 1 or row > 8 or col > 8 or value > 9:
        return False

    # Check for matching numbers in the row or column
    for parse in range(9):
        if board[row][parse] == value:
            return False

        if board[parse][col] == value:
            return False

    # Check for matching numbers in the same box
    box_row = int(row / 3) * 3
    box_col = int(col / 3) * 3
    for row_i in range(3):
        for col_i in range(3):
            if board[box_row + row_i][box_col + col_i] == value:
                return False

    return True


# Inputs: (int) row, (int) column
# Outputs: List
# Returns a list of valid numbers that can be placed at given row and column
def valid_numbers(row, col):

    valid_nums = []

    if board[row][col] != 0:
        return []

    for number in range(1, 10):
        if valid_play(row, col, number):
            valid_nums.append(number)

    return valid_nums


# Inputs: None
# Outputs: success (Boolean)
# Returns true if the board can be solved. False if the board has no solution
# This function implements the backtracking algorithm, in which the board is filled in one-by-one until a square is
# reached that has no solutions. It then backtracks to try other numbers in previous squares until all options are
# exhausted. If the board is valid at any point then it returns true.
def solve_backtracking():
    solve_backtracking_helper(0, 0)
    return valid_board()


# Inputs: (int) row, (int) column
# Outputs: Success at tile (Boolean)
# Helper function to recursively solve the sudoku board
def solve_backtracking_helper(row, col):

    # Check that row and col did not go out of bounds
    if row < 0 or row > 8 or col < 0 or col > 8:
        print("Row or column out of range\nRow: " + row + "\nColumn: " + col)
        return False

    # numbers_to_play holds a list of valid numbers at this tile
    numbers_to_play = valid_numbers(row, col)

    if not numbers_to_play:
        # There are no valid numbers
        if board[row][col] != 0:
            # If there was already a number there, move forward
            if col == 8:
                if solve_backtracking_helper(row + 1, 0):
                    return True
            else:
                if solve_backtracking_helper(row, col + 1):
                    return True

            # The numbers after this did not work. Backtrack
            return False

        else:
            # No possible numbers and empty square. Need to backtrack
            return False

    if numbers_to_play and row == 8 and col == 8:
        # List has an option to place at this square and the game is finished
        # There should only be one valid number to place
        board[row][col] = numbers_to_play[0]
        return True

    for i in numbers_to_play:
        # try all numbers
        board[row][col] = i;

        # Move on to see if the rest of the board can be solved
        if col == 8:
            if solve_backtracking_helper(row + 1, 0):
                return True
        else:
            if solve_backtracking_helper(row, col + 1):
                return True

        # This number did not work continue to the next one
        board[row][col] = 0

    # If the function reached this point then it has exhausted all possible numbers in this position without success
    return False


# Inputs: None
# Outputs: valid (Boolean)
# Returns true if all of the non-zero spaces on the board are valid
def valid_board():
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                prev_num = board[row][col]
                board[row][col] = 0
                if not valid_play(row, col, prev_num):
                    board[row][col] = prev_num
                    # print("Invalid value at " + row + ", " + col)
                    return False
                board[row][col] = prev_num

    return True


board = array([[0, 0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 8, 0, 0, 0, 0],
               [2, 0, 9, 0, 0, 0, 0, 0, 7],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 3, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]])

print(solve_backtracking())

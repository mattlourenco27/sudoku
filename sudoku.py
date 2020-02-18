# Created on 18 Feb 2020
# Created by: Matthew Lourenco
# This is a program that simulates sudoku
from typing import List

def valid_play(row, col, value):

    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(value, int)

    # Check for existing number
    if board[row][col] != 0:
        return False

    # Check for valid bounds
    if row < 0 or col < 0 or value < 1 or row > 8 or col > 8 or value > 9 :
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

board: List[List[int]] = [[0, 0, 0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 6, 0, 0, 0],
                          [0, 0, 0, 4, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 8, 0, 0, 0, 0],
                          [2, 0, 9, 0, 0, 0, 0, 0, 7],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 3, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0]]


#print(valid_play(0, 6, 2))
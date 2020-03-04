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
import pygame


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

    global board

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
        board[row][col] = i

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


# Inputs: None
# Outputs: None
# Prints the board to the console
def print_board():
    for row in range(9):
        if row % 3 == 0:
            print("+---+---+---+")
        for col in range(9):
            if col % 3 == 0:
                print('|', end='')
            print(board[row][col], end='')
        print("|")
    print("+---+---+---+")


# Inputs: None
# Outputs: None
# Sets up the display surface
def setup_display():
    screen.fill(LIGHT_GREY)

    # Draw the row dividers
    for row_divider in range(1, 9):
        line_width = 3
        if row_divider % 3 == 0:
            line_width = 5

        channel_width = SCREEN_SIZE[1] / 9

        pygame.draw.line(screen, BLACK,
                         (0, row_divider * channel_width),
                         (SCREEN_SIZE[0], row_divider * channel_width),
                         line_width)

    # Draw the column dividers
    for col_divider in range(1, 9):
        line_width = 3
        if col_divider % 3 == 0:
            line_width = 5

        channel_width = SCREEN_SIZE[0] / 9

        pygame.draw.line(screen, BLACK,
                         (col_divider * channel_width, 0),
                         (col_divider * channel_width, SCREEN_SIZE[1]),
                         line_width)

    pygame.display.update()


# Inputs: None
# Outputs: None
# Draws the board to the display
def draw_board():
    setup_display()

    text = pygame.font.Font(None, 80)
    channel_width = SCREEN_SIZE[0] / 9
    channel_height = SCREEN_SIZE[1] / 9

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                text_surface = text.render(str(board[row][col]), True, BLACK)
                text_rect = text_surface.get_rect()
                text_rect.center = ((col + 0.5) * channel_width, (row + 0.5) * channel_height)
                screen.blit(text_surface, text_rect)
    pygame.display.update()


# Inputs: (int) row, (int) column
# Outputs: None
# Draws a highlighted box at given row and column
def draw_highlight(col, row):
    channel_width = SCREEN_SIZE[0] / 9
    channel_height = SCREEN_SIZE[1] / 9
    points = [(col * channel_width, row * channel_height),
              ((col + 1) * channel_width, row * channel_height),
              ((col + 1) * channel_width, (row + 1) * channel_height),
              (col * channel_width, (row + 1) * channel_height)]
    pygame.draw.lines(screen, LIME, True, points, 5)
    pygame.display.update()


# Inputs: None
# Outputs: None
# Controls the game event loop
def game_loop():
    global clicked_tile

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                # Solve the sudoku board
                if event.key == pygame.K_RETURN:
                    solve_backtracking()
                    draw_board()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set the clicked tile. Highlight it when mouse up
                if pygame.mouse.get_pressed()[0]:
                    clicked_tile[0] = int(pygame.mouse.get_pos()[0] / SCREEN_SIZE[0] * 9)
                    clicked_tile[1] = int(pygame.mouse.get_pos()[1] / SCREEN_SIZE[1] * 9)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Highlight the clicked tile if the mouse was not moved
                if not pygame.mouse.get_pressed()[0]:
                    temp = [int(pygame.mouse.get_pos()[0] / SCREEN_SIZE[0] * 9),
                            int(pygame.mouse.get_pos()[1] / SCREEN_SIZE[1] * 9)]
                    if temp == clicked_tile:
                        # If mouse up in same tile highlight it
                        draw_highlight(clicked_tile[0], clicked_tile[1])
                    else:
                        # Else do not highlight it
                        setup_display()
                        draw_board()


board = array([[0, 0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 6, 0, 0, 0],
               [0, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 8, 0, 0, 0, 0],
               [2, 0, 9, 0, 0, 0, 0, 0, 7],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 3, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Board that the user will edit when attempting to solve
usr_board = board

# Defined constants
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
LIME = (0, 255, 0)
SCREEN_SIZE = (600, 600)

# Globals
clicked_tile = [0, 0]

# Initialize the game
pygame.init()

pygame.display.set_caption("'Sudoku' made by mattlourenco27 on Github")
# Icon made by Freepik from www.flaticon.com
icon = pygame.image.load("./assets/sprites/icon.png")
pygame.display.set_icon(icon)

# Create the screen
screen = pygame.display.set_mode(SCREEN_SIZE)

setup_display()
draw_board()
game_loop()

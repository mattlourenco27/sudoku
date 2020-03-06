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

from copy import deepcopy
import random

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
    return solved_board()


# Inputs: (int) row, (int) column
# Outputs: Success at tile (Boolean)
# Helper function to recursively solve the sudoku board
def solve_backtracking_helper(row, col):
    # Check that row and col did not go out of bounds
    if row < 0 or row > 8 or col < 0 or col > 8:
        print("Row or column out of range\nRow: " + str(row) + "\nColumn: " + str(col))
        return False

    global board

    # numbers_to_play holds a list of valid numbers at this tile
    numbers_to_play = valid_numbers(row, col)

    if not numbers_to_play:
        # There are no valid numbers
        if board[row][col] != 0 and row == 8 and col ==8:
            # At the end of the board, success
            return True

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

        # Step through the process if requested
        if step_solve:
            draw_display((0, 0))
            pygame.time.wait(25)

            # Allow quit signal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game
                    pygame.quit()
                    quit()

        # Move on to see if the rest of the board can be solved
        if col == 8:
            if solve_backtracking_helper(row + 1, 0):
                return True
        else:
            if solve_backtracking_helper(row, col + 1):
                return True

        # This number did not work continue to the next one
        board[row][col] = 0

        # Step through the process if requested
        if step_solve:
            draw_display((0, 0))
            pygame.time.wait(25)

            # Allow quit signal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game
                    pygame.quit()
                    quit()

    # If the function reached this point then it has exhausted all possible numbers in this position without success
    return False


# Inputs: None
# Outputs: valid (Boolean)
# Returns true if all of the non-zero spaces on the board are valid
def valid_board():
    global board

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0 and template[row][col] == 0:
                prev_num = board[row][col]
                board[row][col] = 0
                if not valid_play(row, col, prev_num):
                    # This number was not a valid play at this position
                    board[row][col] = prev_num

                    # Check for 'check_placed' flag to update graphics
                    if check_placed:
                        channel_width = SCREEN_SIZE[0] / 9
                        channel_height = SCREEN_SIZE[1] / 9

                        # Transparent surface
                        overlay = pygame.Surface((int(channel_width), int(channel_height)), pygame.SRCALPHA)
                        overlay.fill((255, 0, 0, 63))

                        screen.blit(overlay, (int(col * channel_width), int(row * channel_height)))

                    return False
                board[row][col] = prev_num

    return True


# Inputs: None
# Outputs: valid (Boolean)
# Returns true if the board has been solved
def solved_board():
    global board

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                # Board is not filled in
                return False
            if template[row][col] == 0:
                prev_num = board[row][col]
                board[row][col] = 0
                if not valid_play(row, col, prev_num):
                    # This number was not a valid play at this position
                    board[row][col] = prev_num
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
                         (0, int(row_divider * channel_width)),
                         (SCREEN_SIZE[0], int(row_divider * channel_width)),
                         line_width)

    # Draw the column dividers
    for col_divider in range(1, 9):
        line_width = 3
        if col_divider % 3 == 0:
            line_width = 5

        channel_width = SCREEN_SIZE[0] / 9

        pygame.draw.line(screen, BLACK,
                         (int(col_divider * channel_width), 0),
                         (int(col_divider * channel_width), SCREEN_SIZE[1]),
                         line_width)


# Inputs: None
# Outputs: None
# Draws the board to the display
def draw_board():
    text = pygame.font.Font(None, 80)
    channel_width = SCREEN_SIZE[0] / 9
    channel_height = SCREEN_SIZE[1] / 9

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                colour = BLACK
                if template[row][col] == 0:
                    colour = (100, 100, 100)
                text_surface = text.render(str(board[row][col]), True, colour)
                text_rect = text_surface.get_rect()
                text_rect.center = (int((col + 0.5) * channel_width), int((row + 0.5) * channel_height))
                screen.blit(text_surface, text_rect)


# Inputs: (int) row, (int) column
# Outputs: None
# Draws a highlighted box at given row and column
def draw_highlight(col, row):
    if row < 0 or row > 8 or col < 0 or col > 8 or not draw_highlight_tile: return

    channel_width = SCREEN_SIZE[0] / 9
    channel_height = SCREEN_SIZE[1] / 9
    points = [(int(col * channel_width), int(row * channel_height)),
              (int((col + 1) * channel_width), int(row * channel_height)),
              (int((col + 1) * channel_width), int((row + 1) * channel_height)),
              (int(col * channel_width), int((row + 1) * channel_height))]
    pygame.draw.lines(screen, LIME, True, points, 5)


# Inputs: Mouse position (tuple)
# Outputs: None
# Draws the sidebar for the game
def draw_sidebar(mouse):
    x_off = SCREEN_SIZE[0]  # X offset to the sidebar
    pygame.draw.line(screen, BLACK, (x_off, 0), SCREEN_SIZE, 5)

    # Set up text
    text = pygame.font.Font(None, 28)

    # Solve board button
    rect = pygame.Rect(x_off + 25, 25, 150, 50)
    if rect.collidepoint(mouse): pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 5)
    text_surface = text.render("Auto-Solve", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)

    # Step-solve button
    rect = rect.move(0, 75)
    if rect.collidepoint(mouse): pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 5)
    text_surface = text.render("Step-Solve", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)

    # Check-Solved button
    rect = rect.move(0, 75)
    if rect.collidepoint(mouse): pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 5)
    text_surface = text.render("Check Solved", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)

    # Check-Placed button
    rect = rect.move(0, 75)
    if rect.collidepoint(mouse): pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 5)
    text_surface = text.render("Check Placed", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)

    # Rand Board button
    rect = rect.move(0, 75)
    if rect.collidepoint(mouse): pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 5)
    text_surface = text.render("Rand Board", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)

    # Restart button
    rect = rect.move(0, 75)
    if rect.collidepoint(mouse): pygame.draw.rect(screen, WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 5)
    text_surface = text.render("Restart", True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)


# Inputs: Mouse position (tuple)
# Outputs: None
# Draws the display every cycle
def draw_display(mouse):
    setup_display()
    draw_sidebar(mouse)
    draw_board()
    draw_highlight(highlight_tile[0], highlight_tile[1])

    pygame.display.update()


# Inputs: Mouse position (tuple)
# Outputs: None
# Handles mouse clicking when inside sidebar
def sidebar_mouse_handle(mouse):
    global board
    global template
    global solved
    global step_solve
    global pause_time
    global check_placed
    global highlight_tile
    global draw_highlight_tile

    x_off = SCREEN_SIZE[0]  # X offset to the sidebar
    solve_rect = pygame.Rect(x_off + 25, 25, 150, 50)
    step_solve_rect = solve_rect.move(0, 75)
    check_solved_rect = step_solve_rect.move(0, 75)
    check_placed_rect = check_solved_rect.move(0, 75)
    rand_board_rect = check_placed_rect.move(0, 75)
    restart_rect = rand_board_rect.move(0, 75)

    if solve_rect.collidepoint(mouse) and not solved:
        board = deepcopy(template)
        solved = solve_backtracking()

    if step_solve_rect.collidepoint(mouse) and not solved:
        step_solve = True
        board = deepcopy(template)
        solved = solve_backtracking()
        step_solve = False

    if check_solved_rect.collidepoint(mouse):
        pause_time = 1000  # 1 sec
        points = [(0, 0), (SCREEN_SIZE[0], 0), SCREEN_SIZE, (0, SCREEN_SIZE[1])]

        # Choose colour based on if the board is valid
        colour = RED
        if solved_board():
            colour = LIME

        pygame.draw.lines(screen, colour, True, points, 7)
        pygame.display.update()

    if check_placed_rect.collidepoint(mouse):
        pause_time = 1000  # 1 sec
        points = [(0, 0), (SCREEN_SIZE[0], 0), SCREEN_SIZE, (0, SCREEN_SIZE[1])]

        # Remove highlights
        highlight_tile = [-1, -1]
        draw_highlight_tile = False
        draw_display(mouse)

        check_placed = True

        # Choose colour based on if the board is valid
        colour = RED
        if valid_board():
            colour = LIME

        check_placed = False

        pygame.draw.lines(screen, colour, True, points, 7)
        pygame.display.update()

    if rand_board_rect.collidepoint(mouse):
        template = deepcopy(template_boards[random.randint(0, 4)])
        solved = False
        board = deepcopy(template)

    if restart_rect.collidepoint(mouse):
        solved = False
        board = deepcopy(template)


# Inputs: None
# Outputs: None
# Controls the game event loop
def game_loop():
    global highlight_tile
    global draw_highlight_tile
    global board
    global pause_time

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Exit the game
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Set the clicked tile. Highlight it when mouse up
                if pygame.mouse.get_pressed()[0]:
                    # Check if mouse is over the sidebar
                    rect = pygame.Rect(SCREEN_SIZE[0], 0, SIDE_BAR, SCREEN_SIZE[1])
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        sidebar_mouse_handle(pygame.mouse.get_pos())
                    else:
                        temp = [int(pygame.mouse.get_pos()[0] / SCREEN_SIZE[0] * 9),
                                int(pygame.mouse.get_pos()[1] / SCREEN_SIZE[1] * 9)]
                        if temp == highlight_tile:
                            draw_highlight_tile = False
                            highlight_tile[0] = -1
                            highlight_tile[1] = -1
                        elif temp[0] >= 0 and temp[0] <= 8 and temp[1] >= 0 and temp[1] <= 8:
                            highlight_tile[0] = temp[0]
                            highlight_tile[1] = temp[1]

            elif event.type == pygame.MOUSEBUTTONUP:
                # Highlight the clicked tile if the mouse was not moved
                if not pygame.mouse.get_pressed()[0]:
                    temp = [int(pygame.mouse.get_pos()[0] / SCREEN_SIZE[0] * 9),
                            int(pygame.mouse.get_pos()[1] / SCREEN_SIZE[1] * 9)]
                    if temp == highlight_tile:
                        # If mouse up in same tile, highlight
                        draw_highlight_tile = True
                    else:
                        # Else do not highlight it
                        highlight_tile = [-1, -1]

            elif event.type == pygame.KEYUP:
                # If a tile is highlighted and the highlighted tile can be changed, change it
                if highlight_tile[0] != -1 and highlight_tile[1] != -1 and template[highlight_tile[1]][
                    highlight_tile[0]] == 0:
                    if event.key == pygame.K_0 or event.key == pygame.K_BACKSPACE:
                        board[highlight_tile[1]][highlight_tile[0]] = 0
                    elif event.key == pygame.K_1:
                        board[highlight_tile[1]][highlight_tile[0]] = 1
                    elif event.key == pygame.K_2:
                        board[highlight_tile[1]][highlight_tile[0]] = 2
                    elif event.key == pygame.K_3:
                        board[highlight_tile[1]][highlight_tile[0]] = 3
                    elif event.key == pygame.K_4:
                        board[highlight_tile[1]][highlight_tile[0]] = 4
                    elif event.key == pygame.K_5:
                        board[highlight_tile[1]][highlight_tile[0]] = 5
                    elif event.key == pygame.K_6:
                        board[highlight_tile[1]][highlight_tile[0]] = 6
                    elif event.key == pygame.K_7:
                        board[highlight_tile[1]][highlight_tile[0]] = 7
                    elif event.key == pygame.K_8:
                        board[highlight_tile[1]][highlight_tile[0]] = 8
                    elif event.key == pygame.K_9:
                        board[highlight_tile[1]][highlight_tile[0]] = 9

        if pause_time:
            pygame.time.wait(pause_time)
            pause_time = 0

        mouse = pygame.mouse.get_pos()
        draw_display(mouse)
        clock.tick(60)


template_boards = [[[0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 6, 0, 0, 0],
                    [0, 0, 0, 4, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 8, 0, 0, 0, 0],
                    [2, 0, 9, 0, 0, 0, 0, 0, 7],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 3, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]],

                   [[0, 6, 0, 3, 0, 0, 8, 0, 4],
                    [5, 3, 7, 0, 9, 0, 0, 0, 0],
                    [0, 4, 0, 0, 0, 6, 3, 0, 7],
                    [0, 9, 0, 0, 5, 1, 2, 3, 8],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [7, 1, 3, 6, 2, 0, 0, 4, 0],
                    [3, 0, 6, 4, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 6, 0, 5, 2, 3],
                    [1, 0, 2, 0, 0, 9, 0, 8, 0]],

                   [[0, 0, 0, 0, 0, 7, 0, 0, 0],
                    [0, 0, 2, 4, 0, 6, 3, 0, 0],
                    [0, 1, 7, 0, 0, 0, 9, 6, 0],
                    [5, 8, 0, 0, 0, 0, 0, 3, 0],
                    [0, 0, 0, 0, 9, 0, 0, 0, 0],
                    [0, 7, 0, 0, 0, 0, 0, 4, 2],
                    [0, 9, 4, 0, 0, 0, 6, 5, 0],
                    [0, 0, 5, 2, 0, 8, 1, 0, 0],
                    [0, 0, 0, 5, 0, 0, 0, 0, 0]],

                   [[0, 9, 0, 0, 0, 3, 6, 0, 0],
                    [0, 0, 0, 1, 0, 0, 2, 0, 0],
                    [3, 0, 2, 0, 0, 6, 0, 9, 8],
                    [0, 0, 0, 0, 0, 0, 1, 2, 5],
                    [0, 0, 4, 0, 0, 0, 8, 0, 0],
                    [5, 2, 9, 0, 0, 0, 0, 0, 0],
                    [2, 4, 0, 7, 0, 0, 5, 0, 3],
                    [0, 0, 3, 0, 0, 2, 0, 0, 0],
                    [0, 0, 8, 3, 0, 0, 0, 1, 0]],

                   [[1, 0, 0, 2, 0, 0, 3, 0, 0],
                    [2, 0, 0, 3, 0, 0, 4, 0, 0],
                    [3, 0, 0, 4, 0, 0, 5, 0, 0],
                    [4, 0, 0, 5, 0, 0, 6, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 3, 0, 0, 4, 0, 0, 5],
                    [0, 0, 4, 0, 0, 5, 0, 0, 6],
                    [0, 0, 5, 0, 0, 6, 0, 0, 7],
                    [0, 0, 6, 0, 0, 7, 0, 0, 8]]]

template = deepcopy(template_boards[0])

# Board that the user will edit when attempting to solve
board = deepcopy(template)

# Defined constants
WHITE = (255, 255, 255)
LIGHT_GREY = (240, 240, 240)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME = (0, 255, 0)
SCREEN_SIZE = (600, 600)
SIDE_BAR = 200

# Globals and Flags
highlight_tile = [-1, -1]
draw_highlight_tile = False
solved = False
step_solve = False
check_placed = False
pause_time = 0  # Time to pause after this event loop in milliseconds

# Initialize the game
pygame.init()

pygame.display.set_caption("'Sudoku' made by mattlourenco27 on Github")
# Icon made by Freepik from www.flaticon.com
icon = pygame.image.load("./assets/sprites/icon.png")
pygame.display.set_icon(icon)

# Create the game clock
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((SCREEN_SIZE[0] + SIDE_BAR, SCREEN_SIZE[1]))

draw_display((0, 0))
game_loop()

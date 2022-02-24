# This file was almost entirely created from suggestions of GitHub Copilot
# The prompt was the following:
#
# conway game of life

from pprint import pprint

def conway(board):
    """
    conway game of life
    """
    # create a copy of the board
    new_board = [list(x) for x in board]
    # loop through the board
    for i in range(len(board)):
        for j in range(len(board[0])):
            # count the number of neighbors
            neighbors = 0
            for x in range(i-1, i+2):
                for y in range(j-1, j+2):
                    if x == i and y == j:
                        continue
                    if x < 0 or x >= len(board):
                        continue
                    if y < 0 or y >= len(board[0]):
                        continue
                    neighbors += board[x][y]
            # apply rules
            if board[i][j] == 1 and (neighbors < 2 or neighbors > 3):
                new_board[i][j] = 0
            elif board[i][j] == 0 and neighbors == 3:
                new_board[i][j] = 1
    return new_board

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]


def multi_conway(board, n):
    """
    conway game of life
    """
    for i in range(n):
        board = conway(board)
    return board

new_board = conway(board)
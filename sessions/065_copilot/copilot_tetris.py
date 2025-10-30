# This file was almost entirely created from suggestions of GitHub Copilot
# It is not fully functional but starting to add missing functions will cause Copilot to make sensible suggsetions :)
# The prompt was the following:
#
# """This is tetris."""

"""This is tetris."""
import pygame
import random
import time
import sys
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.text as mtext
import matplotlib.font_manager as font_manager
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import matplotlib.patheffects as path_effects
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

WIDTH=800
HEIGHT=600
BOARD_WIDTH=400
BOARD_HEIGHT=200
BLOCK_SIZE=20
SCREEN_WIDTH=800
SCREEN_HEIGHT=600

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Board:
    """Board class of tetris."""
    def __init__(self):
        """Initialize the board."""
        self.board = []
        for i in range(BOARD_WIDTH):
            self.board.append([])
            for j in range(BOARD_HEIGHT):
                self.board[i].append(0)
        self.score = 0
        self.game_over = False
        self.block = Block(BLUE, 1, self)
        self.next_block = Block(RED, 2, self)
        self.block_x = 0
        self.block_y = 0
        self.block_rotation = 0
        self.block_shape = []
        self.block_width = 0
        self.block_height = 0
        self.block_rotations = []
        self.block_rotations.append([])
        self.block_rotations.append([])
        self.block_rotations.append([])
        self.block_rotations.append([])
        self.block_rotations[0].append([])
        self.block_rotations[0].append([])
        self.block_rotations[0].append([])
        self.block_rotations[0].append([])
        self.block_rotations[1].append([])
        self.block_rotations[1].append([])
        self.block_rotations[1].append([])
        self.block_rotations[1].append([])
        self.block_rotations[2].append([])
        self.block_rotations[2].append([])
        self.block_rotations[2].append([])
        self.block_rotations[2].append([])
        self.block_rotations[3].append([])
        self.block_rotations[3].append([])
        self.block_rotations[3].append([])
        self.block_rotations[3].append([])
        self.next_block_x = 0
        self.next_block_y = 0
        self.next_block_rotation = 0
        self.next_block_shape = []
        self.next_block_width = 0
        self.next_block_height = 0
        self.next_block_rotations = []
        self.next_block_rotations.append([])
        self.next_block_rotations.append([])
        self.next_block_rotations.append([])
        self.next_block_rotations.append([])
        self.next_block_rotations[0].append([])
        self.next_block_rotations[0].append([])
        self.next_block_rotations[0].append([])
        self.next_block_rotations[0].append([])
        self.next_block_rotations[1].append([])
        self.next_block_rotations[1].append([])
        self.next_block_rotations[1].append([])
        self.next_block_rotations[1].append([])
        self.next_block_rotations[2].append([])
        self.next_block_rotations[2].append([])
        self.next_block_rotations[2].append([])
        self.next_block_rotations[2].append([])
        self.next_block_rotations[3].append([])
        self.next_block_rotations[3].append([])
        self.next_block_rotations[3].append([])
        self.next_block_rotations[3].append([])
        self.next_block_rotations[0][0].append(1)
        self.next_block_rotations[0][0].append(1)
        self.next_block_rotations[0][0].append(1)
        self.next_block_rotations[0][0].append(1)
        self.next_block_rotations[1][0].append(1)

    def move_down(self):
        """Move the block down."""
        if self.block_y < BOARD_HEIGHT - 1:
            if self.board[self.block_x][self.block_y + 1] == 0:
                self.block_y += 1
            else:
                self.place_block()
                self.new_block()
        else:
            self.place_block()
            self.new_block()
            

    def draw(self, screen):
        """Draw the board."""
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, BLUE, (i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                elif self.board[i][j] == 2:
                    pygame.draw.rect(screen, RED, (i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def update(self):
        """Update the board."""
        if self.block.update():
            self.score += 1
            for i in range(self.block.width):
                for j in range(self.block.height):
                    if self.block.shape[i][j] == 1:
                        self.board[self.block_x + i][self.block_y + j] = self.block.color
            self.block = self.next_block
            self.next_block = Block(RED, 2, self)
            self.block_x = 0
            self.block_y = 0

    def check_game_over(self):
        """Check if the game is over."""
        for i in range(BOARD_WIDTH):
            if self.board[i][0] != 0:
                self.game_over = True
        return self.game_over

    def check_line(self):
        """Check if there is a line."""
        for i in range(BOARD_HEIGHT):
            line = True
            for j in range(BOARD_WIDTH):
                if self.board[j][i] == 0:
                    line = False
            if line:
                self.score += 1
                for k in range(BOARD_WIDTH):
                    self.board[k][i] = 0
                for k in range(i, 0, -1):
                    for l in range(BOARD_WIDTH):
                        self.board[l][k] = self.board[l][k - 1]
                for l in range(BOARD_WIDTH):
                    self.board[l][0] = 0
        return self.score

    def draw_next_block(self, screen):
        """Draw the next block."""
        for i in range(self.next_block.width):
            for j in range(self.next_block.height):
                if self.next_block.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.next_block.color, (self.next_block_x + i * BLOCK_SIZE, self.next_block_y + j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    
    def draw_block(self, screen):
        """Draw the current block."""
        for i in range(self.block.width):
            for j in range(self.block.height):
                if self.block.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.block.color, (self.block_x + i * BLOCK_SIZE, self.block_y + j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self, screen):
        """Draw the score."""
        score_font = pygame.font.SysFont("Arial", 30)
        score_text = score_font.render("Score: " + str(self.score), True, BLACK)
        screen.blit(score_text, (0, 0))

    def draw_game_over(self, screen):
        """Draw the game over message."""
        game_over_font = pygame.font.SysFont("Arial", 50)

        game_over_text = game_over_font.render("Game Over", True, BLACK)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        screen.blit(game_over_text, game_over_rect)

    def draw_board(self, screen):
        """Draw the board."""
        self.draw(screen)
        self.draw_next_block(screen)
        self.draw_block(screen)
        self.draw_score(screen)

    def draw_game_over_screen(self, screen):
        """Draw the game over screen."""
        self.draw_board(screen)
        self.draw_game_over(screen)
        return False
    
    def get_score(self):
        """Get the score."""
        return self.score


class Block:
    """Block class of tetris."""
    def __init__(self, color, number, board):
        """Initialize the block."""
        self.color = color
        self.number = number
        self.board = board
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.rotations = [
            [[0, 0], [0, 1], [1, 0], [1, 1]],
            [[0, 0], [1, 0], [0, 1], [1, 1]]]
        self.shape = self.rotations[self.rotation]
        self.width = len(self.shape)
        self.height = len(self.shape[0])
        self.falling = False
        self.falling_speed = 0.5
        self.falling_time = 0
        self.falling_start_time = 0
        self.falling_start_y = 0
        self.falling_start_x = 0
        self.falling_start_rotation = 0
        self.falling_start_shape = []
        self.falling_start_width = 0
        self.falling_start_height = 0
        self.falling_start_rotations = []
        self.falling_start_rotations.append([])
        self.falling_start_rotations.append([])
        self.falling_start_rotations.append([])
        self.falling_start_rotations.append([])
        self.falling_start_rotations[0].append([])
        self.falling_start_rotations[0].append([])
        self.falling_start_rotations[0].append([])
        self.falling_start_rotations[0].append([])
        self.falling_start_rotations[1].append([])
        self.falling_start_rotations[1].append([])
        self.falling_start_rotations[1].append([])
        self.falling_start_rotations[1].append([])
        self.falling_start_rotations[2].append([])
        self.falling_start_rotations[2].append([])
        self.falling_start_rotations[2].append([])
        self.falling_start_rotations[2].append([])
        self.falling_start_rotations[3].append([])
        self.falling_start_rotations[3].append([])
        self.falling_start_rotations[3].append([])
        self.falling_start_rotations[3].append([])

    def draw(self, screen):
        """Draw the block."""  
        for i in range(self.width):
            for j in range(self.height):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.color, (self.x + i * BLOCK_SIZE, self.y + j * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def update(self):
        """Update the block."""
        if self.falling:
            self.falling_time += 1
            if self.falling_time > self.falling_start_time + self.falling_speed:
                self.falling_time = 0
                self.y += 1
                if self.y + self.height > BOARD_HEIGHT:
                    self.y = self.falling_start_y
                    self.x = self.falling_start_x
                    self.rotation = self.falling_start_rotation
                    self.shape = self.falling_start_shape
                    self.width = self.falling_start_width
                    self.height = self.falling_start_height
                    self.rotations = self.falling_start_rotations
                    self.falling = False
                    return True
                for i in range(self.width):
                    for j in range(self.height):
                        if self.shape[i][j] == 1:
                            if self.y + j >= BOARD_HEIGHT or self.board[self.x + i][self.y + j] != 0:
                                self.y = self.falling_start_y
                                self.x = self.falling_start_x
                                self.rotation = self.falling_start_rotation
                                self.shape = self.falling_start_shape
                                self.width = self.falling_start_width
                                self.height = self.falling_start_height
                                self.rotations = self.falling_start_rotations
                                self.falling = False
                                return True


def game_loop():
    """Game loop of tetris."""
    # initialize pygame
    pygame.init()
    # set up the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    # set up the clock
    clock = pygame.time.Clock()
    # set up the font
    myfont = pygame.font.SysFont("monospace", 15)

    # set up the blocks
    block_colors = [RED, GREEN, BLUE, YELLOW]
    block_list = []
    # set up the board
    board = Board()
    for i in range(4):
        block_list.append(Block(block_colors[i], i, board))
    # set up the score
    score = 0
    # set up the game loop
    game_over = False
    while not game_over:
        # check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board.move_left()
                elif event.key == pygame.K_RIGHT:
                    board.move_right()
                elif event.key == pygame.K_DOWN:
                    board.move_down()
                elif event.key == pygame.K_UP:
                    board.rotate()
                elif event.key == pygame.K_SPACE:
                    board.drop()
        # draw the screen
        screen.fill(BLACK)
        board.draw(screen)
        # draw the score
        text = myfont.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (10, 10))
        # update the screen
        pygame.display.flip()
        # tick the clock
        clock.tick(60)
        # update the board
        board.update()
        # check if the game is over
        if board.game_over:
            game_over = True
        # update the score
        score += board.get_score()
    # game over message
    text = myfont.render("Game Over", 1, WHITE)
    screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    # update the screen
    pygame.display.flip()
    # wait for a keypress
    pygame.event.wait()

game_loop()
# Örn Ól Strange
# 19.01.2018

import pygame as pg
from random import randint, randrange, choice
from text import text_to_screen
from maze_generator import generate_maze

"""
Cell: i, j, x, y, wall?, show, exit?
Grid: cells[], show, fill_grid
Item: i, j, x, y, type?, show
Player: i, j, x, y, show
Game: show_all, update_pos, reset_level, score

items types = bomb-defuser, bomb, treasure-chest, key

screen size: 720x720
tile size: 16x16
tile count: 45x45

background: black
wall: gray
player: white circle
bomb: red circle
defuser: green circle
chest: brown rect
key: yellow keyshape
exit: wall color closed, background color open
"""

# SETTINGS
TILE_S = 24
TILE_C = 31
SCREEN_W, SCREEN_H = TILE_S*TILE_C, TILE_S*TILE_C
FPS = 120

# COLORS
BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (120, 120, 120)
PLAYER_COLOR = (240, 240, 240)
BOMB_COLOR = (200, 60, 60)
DEFUSER_COLOR = (60, 200, 60)
KEY_COLOR = (60, 200, 200)
CHEST_COLOR = (200, 120, 60)
EXIT_OPEN = BACKGROUND_COLOR
EXIT_CLOSED = WALL_COLOR


class Item:
    def __init__(self, i, j, t):
        self.i = i
        self.j = j
        self.size = TILE_S
        self.x = j * self.size
        self.y = i * self.size
        self.rectangle = pg.Rect(self.x+2, self.y+2, self.size-4, self.size-4)

        self.color = PLAYER_COLOR

        self.t = t

    def show(self):

class Game:
    def __init__(self):
        self.score = 0

        self.grid = Grid()
        self.setup_grid()

        self.items = Items()

        self.player = Player(0, 1)

    def setup_grid(self):
        self.grid.fill_grid(generate_maze(TILE_C))
        self.grid.random_exit()

    def can_player_move(self, direction):
        i = self.player.i
        j = self.player.j
        cells = self.grid.cells
        if direction == "U":
            return (i != 0) and (not cells[i-1][j].wall)
        elif direction == "D":
            return (i != TILE_C-1) and (not cells[i+1][j].wall)
        elif direction == "L":
            return (j != 0) and (not cells[i][j-1].wall)
        elif direction == "R":
            return (j != TILE_C-1) and (not cells[i][j+1].wall)
        return False

    def show_all(self):
        self.grid.show()
        self.player.show()


class Cell:
    def __init__(self, i, j, wall):
        self.i = i
        self.j = j
        self.size = TILE_S
        self.x = j * self.size
        self.y = i * self.size

        self.wall = wall
        self.exit = False

        self.color = WALL_COLOR if wall else BACKGROUND_COLOR

        self.rectangle = pg.Rect(self.x, self.y, self.size, self.size)

    def show(self):
        pg.draw.rect(screen, self.color, self.rectangle)


class Grid:
    def __init__(self):
        self.cells = [["" for j in range(TILE_C)] for i in range(TILE_C)]

    def show(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.show()

    def fill_grid(self, arr):
        for cell_row in range(len(arr)):
            for cell in range(len(arr[cell_row])):
                self.cells[cell_row][cell] = Cell(cell_row, cell, arr[cell_row][cell])

    def random_exit(self):
        index = randrange(1, TILE_C, 2)
        self.cells[-1][index].wall = False
        self.cells[-1][index].exit = True
        self.cells[-1][index].color = EXIT_OPEN


class Player:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.size = TILE_S
        self.x = j * self.size
        self.y = i * self.size
        self.rectangle = pg.Rect(self.x+2, self.y+2, self.size-4, self.size-4)

        self.color = PLAYER_COLOR

    def show(self):
        pg.draw.ellipse(screen, self.color, self.rectangle)

    def move(self, direction):
        if direction == "U":
            self.i -= 1
        elif direction == "D":
            self.i += 1
        elif direction == "L":
            self.j -= 1
        elif direction == "R":
            self.j += 1

        self.update_pos()

    def update_pos(self):
        self.x = self.j * self.size
        self.y = self.i * self.size
        self.rectangle = pg.Rect(self.x + 2, self.y + 2, self.size - 4, self.size - 4)


# INIT
pg.init()
pg.font.init()
clock = pg.time.Clock()
game_loop = True

# screen
screen = pg.display.set_mode((SCREEN_W, SCREEN_H))

game = Game()
grid = game.grid

while game_loop:
    screen.fill(BACKGROUND_COLOR)
    clock.tick(FPS)

    # EVENTS
    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            game_loop = False

        # keys player
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w and game.can_player_move("U"):
                game.player.move("U")
            elif event.key == pg.K_s and game.can_player_move("D"):
                game.player.move("D")
            elif event.key == pg.K_a and game.can_player_move("L"):
                game.player.move("L")
            elif event.key == pg.K_d and game.can_player_move("R"):
                game.player.move("R")

    # GRID
    game.show_all()

    # DISPLAY
    pg.display.flip()
    pg.display.update()

# exit
pg.quit()
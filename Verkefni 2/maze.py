# Örn Ól Strange
# 19.01.2018

from pygame import pygame as pg
from random import randint
from text import text_to_screen
from maze_generator import generate_maze

"""
Cell: i, j, x, y, type?, show, exit?
Grid: cells[], show, fill_grid
Item: i, j, x, y, type?, show
Player: i, j, x, y, show, update_pos
Game: show_all, update_pos, reset_level, score

items types = bomb-defuser, bomb, treasure-chest
cell types = wall, ground, exit

screen size: 720x720
tile size: 16x16
tile count: 45x45

background: black
wall: gray
player: white circle
bomb: red circle
defuser: yellow square
chest: brown square
exit: wall color closed, black open
"""

# SETTINGS
SCREEN_W, SCREEN_H = 720, 720
TILE_S = 16
TILE_C = 45

BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (120, 120, 120)
PLAYER_COLOR = (240, 240, 240)
BOMB_COLOR = (200, 60, 60)
DEFUSER_COLOR = (60, 200, 200)
CHEST_COLOR = (200, 120, 60)
EXIT_OPEN = BACKGROUND_COLOR
EXIT_CLOSED = WALL_COLOR




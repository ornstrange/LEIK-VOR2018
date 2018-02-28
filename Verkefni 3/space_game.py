# Örn Ól Strange
# 28.02.2018

import pygame as pg
from random import randint, randrange, choice, shuffle
from text import text_to_screen
from maze_generator import generate_maze
import sys

"""
Entity: x,y, xvel,yvel, sprite/repr, hitw, hith,
Player(Entity): keys/move, shoot
Enemy(Entity): move, die, speed, type
Game: game_logic, [entitites], player
"""


class Entity(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()

        self.xvel = kwargs.get('xvel', 0)
        self.yvel = kwargs.get('yvel', 0)
        self.w = kwargs.get('hitw', 0)
        self.h = kwargs.get('hith', 0)
        self.color = kwargs.get('col', (255, 0, 0))

        self.image = pg.Surface([self.w, self.h])
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = kwargs.get('x', 0)
        self.rect.y = kwargs.get('y', 0)

        self.sprite = False
        self.sprite_file = ""

    def set_sprite(self, filename):
        self.sprite = True
        self.sprite_file = filename

    def __repr__(self):
        return "Entity at X: %d, Y: %d" % (self.x, self.y)

    def show(self):
        if self.sprite:
            self.image = pg.image.load(self.sprite_file).convert_alpha()
        else:
            pg.draw.rect(self.image, self.color, [self.x, self.y, self.w, self.h])


BACKGROUND_COLOR = (230, 230, 230)
FPS = 60

# INIT
pg.init()
pg.font.init()
clock = pg.time.Clock()
game_loop = True

# screen
screen = pg.display.set_mode((480, 360))

dude = Entity(x=50, y=50, w=50, h=50)
sprites = pg.sprite.Group()
sprites.add(dude)

while game_loop:
    screen.fill(BACKGROUND_COLOR)
    clock.tick(FPS)

    # EVENTS
    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            game_loop = False

    sprites.update()
    sprites.draw(screen)

    # DISPLAY
    pg.display.flip()
    pg.display.update()

# exit
pg.quit()

# -*- coding: utf-8 -*-
# Örn Ól Strange
# 28.02.2018

import pygame as pg
from random import randint, randrange, choice, shuffle
from text import text_to_screen
import sys

"""
Entity: x,y, xvel,yvel, sprite/repr, hitw, hith,
Player(Entity): keys/move, shoot
Enemy(Entity): move, die, speed, type
Game: game_logic, [entitites], player
"""


class Entity(object):
    def __init__(self, **kwargs):
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.xvel = kwargs.get('xvel', 0)
        self.yvel = kwargs.get('yvel', 0)
        self.w = kwargs.get('w', 0)
        self.h = kwargs.get('h', 0)
        self.color = kwargs.get('col', (230, 0, 0))
        self.dir = "U"
        self.speed = PLAYER_SPEED

        self.collision_rect = pg.Rect(self.x, self.y, self.w, self.h)

    def __repr__(self):
        return "Entity at X: %d, Y: %d" % (self.x, self.y)

    def update_dir(self):
        if self.xvel > 0:
            self.dir += "R" if "R" not in self.dir else ""
        elif self.xvel < 0:
            self.dir += "L" if "L" not in self.dir else ""
        else:
            self.dir = self.dir.replace("R", "").replace("L", "") if len(self.dir) > 1 else self.dir
        if self.yvel > 0:
            self.dir += "D" if "D" not in self.dir else ""
        elif self.yvel < 0:
            self.dir += "U" if "U" not in self.dir else ""
        else:
            self.dir = self.dir.replace("U", "").replace("D", "") if len(self.dir) > 1 else self.dir
        self.dir = self.dir[:2] if len(self.dir) > 2 else self.dir

    def velocity_check(self):
        if self.xvel != 0 and self.yvel != 0:
            self.speed = int(PLAYER_SPEED * ((2**0.5) - 1))
        else:
            self.speed = PLAYER_SPEED

    def update_pos(self):
        self.velocity_check()
        self.update_dir()
        self.collision_rect.width = self.w
        self.collision_rect.height = self.h
        self.collision_rect.move_ip(self.xvel, self.yvel)
        self.x = self.collision_rect.x
        self.y = self.collision_rect.y

    def show(self):
        print(self.dir)
        self.update_pos()
        pg.draw.rect(screen, self.color, self.collision_rect)



class Player(Entity):
    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

BACKGROUND_COLOR = (230, 230, 230)
FPS = 60
PLAYER_SPEED = 3

# INIT
pg.init()
pg.font.init()
pg.key.set_repeat(50, 10)
clock = pg.time.Clock()
game_loop = True

# screen
screen = pg.display.set_mode((448, 512))

player = Player(x=50, y=50, w=32, h=32, col=(125,0,250))

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
            if event.key == pg.K_DOWN:
                player.yvel = player.speed
            elif event.key == pg.K_UP:
                player.yvel = -player.speed
            if event.key == pg.K_RIGHT:
                player.xvel = player.speed
            elif event.key == pg.K_LEFT:
                player.xvel = -player.speed
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_UP, pg.K_DOWN]:
                player.yvel = 0
            elif event.key in [pg.K_RIGHT, pg.K_LEFT]:
                player.xvel = 0

    player.show()

    # DISPLAY
    pg.display.flip()
    pg.display.update()

# exit
pg.quit()

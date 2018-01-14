# Örn Óli Strange
# YAHTZEE - 12.01.18

import pygame as pg
from random import randint
from rounded import rounded_rect
from text import text_to_screen
import os

"""
5 teningar, 2 uppi, 3 niðri
2 takkar, kasta aftur og ljúka kasti.
kasti lýkur sjálfkrafa ef búið er að kasta tvisvar.
"""

# init stuff
pg.init()
pg.font.init()
game = True

# screen
screen_width = 480
screen_height = 360
screen = pg.display.set_mode((screen_width, screen_height))
screen_color = (100, 100, 100)
OFFSET = 30


class Dot:
    def __init__(self, val, x, y):
        self.x = x
        self.y = y

        self.cords = [
            [
                (self.x + 15 + 7, self.y + 15 + 7, 16, 16),
                "",
                (self.x + 15 + 7 + 40, self.y + 15 + 7, 16, 16)
            ],
            [
                (self.x + 15 + 7, self.y + 37 + 7, 16, 16),
                (self.x + 15 + 7 + 20, self.y + 37 + 7, 16, 16),
                (self.x + 15 + 7 + 40, self.y + 37 + 7, 16, 16)
            ],
            [
                (self.x + 15 + 7, self.y + 59 + 7, 16, 16),
                "",
                (self.x + 15 + 7 + 40, self.y + 59 + 7, 16, 16)
            ]
        ]

        self.dots = [
            [(1, 1)],
            [(0, 2), (2, 0)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 0), (0, 2), (2, 0), (2, 2)],
            [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
            [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)],
        ]

        self.val = val

    def show(self):
        current = self.dots[self.val - 1]

        for p in current:
            rounded_rect(screen, (60, 60, 60), self.cords[p[0]][p[1]], 0.8)


class Die:
    def __init__(self, i, j, fake=False):
        self.value = 0
        self.marked = False
        self.clicked = False
        self.fake = fake

        self.paddx = 60
        self.paddy = 20
        self.size = 100
        self.y = (i * self.size) + (i * self.paddy) + OFFSET
        self.x = (j * self.size) + (j * self.paddx) + OFFSET

        self.dots = Dot(self.value, self.x, self.y)

        self.square = (self.x, self.y, self.size, self.size)

    def roll(self):
        self.value = randint(1, 6)
        self.dots.val = self.value

    def show(self):
        if not self.fake:
            color = (230, 230, 230) if not self.marked else (190, 190, 190)
            rounded_rect(screen, color, self.square, 0.2)
            self.dots.show()

    def contains(self):
        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]
        return (self.x <= mouse_x <= self.x + self.size) and (self.y <= mouse_y <= self.y + self.size)

    def mouse(self):
        m_click = pg.mouse.get_pressed()[0]
        if self.contains():
            if m_click and not self.clicked:
                self.marked = True if not self.marked else False
            elif self.clicked:
                self.clicked = False

class Grid:
    def __init__(self):
        self.dice = [[Die(0, 0), Die(0, 1), Die(0, 2, True)], [Die(1, 0), Die(1, 1), Die(1, 2)]]
        self.buttons = [Button(20, 300, 210, 40, (240, 180, 180), "END TURN", self.roll_all),
                        Button(250, 300, 210, 40, (180, 240, 180), "ROLL AGAIN", self.roll_all)]

    def show_all(self):
        for i in range(2):
            for j in range(3):
                self.dice[i][j].show()
            self.buttons[i].show()

    def roll_all(self):
        for i in range(2):
            for j in range(3):
                if not self.dice[i][j].marked:
                    self.dice[i][j].roll()

    def mouse_events(self):
        for i in range(2):
            for j in range(3):
                self.dice[i][j].mouse()
            self.buttons[i].mouse()


class Button:
    def __init__(self, x, y, w, h, col, name, func):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.col = col
        self.name = name

        self.func = func

    def show(self):
        rounded_rect(screen, self.col, (self.x, self.y, self.w, self.h), 0.2)
        text_to_screen(screen, self.name, self.x + self.w / 2 - 40, self.y + 10, 16, (30, 30, 30))

    def contains(self):
        mouse_x = pg.mouse.get_pos()[0]
        mouse_y = pg.mouse.get_pos()[1]
        return (self.x <= mouse_x <= self.x + self.w) and (self.y <= mouse_y <= self.y + self.h)

    def mouse(self):
        if self.contains():
            if pg.mouse.get_pressed()[0]:
                self.func()


grid = Grid()

grid.roll_all()

while game:
    screen.fill(screen_color)

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            game = False

    grid.show_all()
    grid.mouse_events()

    pg.display.flip()
    pg.display.update()

# exit
pg.quit()

# Örn Óli Strange
# GATHER - 17.01.18

import pygame as pg
from random import randint
from rounded import rounded_rect
from text import text_to_screen

"""
Balls: array af Ball objects
Ball object sem detta úr random position úr toppnum, random size
Ball: vel, x, y, radius
Bretti object sem stækkar þegar boltar lenda á því
Bretti: vel, x, y, width, height, collision_detection
hröðun á fallandi kúlum

win condition er Bretti: width == skjár width
"""

# init stuff
pg.init()
pg.font.init()
clock = pg.time.Clock()
game = True

# screen
screen_width = 600
screen_height = 800
screen = pg.display.set_mode((screen_width, screen_height))
screen_color = (20, 20, 20)


class Paddle:
    def __init__(self):
        self.w = 80
        self.h = 20
        self.x = screen_width / 2 - self.w / 2
        self.y = screen_height - 40
        self.x_vel = 0

    def show(self):
        pg.draw.rect(screen, (230, 230, 230), (self.x, self.y, self.w, self.h))

    def update_pos(self):
        self.x += self.x_vel if 0 <= self.x + self.x_vel <= screen_width - self.w else 0
        self.x_vel = self.x_vel * paddle_acc

    def grow(self):
        if self.x + (self.w + 20) <= screen_width:
            self.w += 20
        else:
            self.x = screen_width - (self.w + 10)
            self.w += 20

        if (self.x - 10) >= 0:
            self.x -= 10
        else:
            self.x = 0

        if self.w >= screen_width:
            global game
            game = False
            print("ÞÚ VANNST!")


class Ball:
    def __init__(self, x, r, col):
        self.x = x
        self.y = -20
        self.rad = r
        self.y_vel = ball_speed

        self.col = col

    def show(self):
        pg.draw.circle(screen, self.col, (self.x, self.y), self.rad)

    def update_pos(self):
        self.y += int(self.y_vel)
        self.y_vel = round(self.y_vel * ball_acc, 2)


class Items:
    def __init__(self):
        self.balls = []
        self.paddle = Paddle()
        self.hider = pg.Rect(0, screen_height - 20, screen_width, 20)

    def update_pos(self):
        for i in self.balls:
            i.update_pos()
        self.paddle.update_pos()

    def add_ball(self):
        random_color = (randint(80, 230), randint(80, 230), randint(80, 230))
        self.balls.append(Ball(randint(40, screen_width - 40), 15, random_color))

    def remove_ball(self, ind):
        if self.balls[ind]:
            self.balls.pop(ind)

    def collision(self):
        paddle = self.paddle

        for i in range(len(self.balls) - 1, -1, -1):
            ball = self.balls[i]
            if ball.y >= screen_height - 20:
                if paddle.x <= ball.x - ball.rad/2 and ball.x + ball.rad/2 <= paddle.x + paddle.w:
                    self.paddle.grow()
                    self.remove_ball(i)
                else:
                    self.__init__()  # reset game
                    print("ÞÚ TAPAÐIR!")

    def show_all(self):
        for i in self.balls:
            i.show()
        self.paddle.show()

        pg.draw.rect(screen, screen_color, self.hider)


items = Items()
paddle_speed = 5
ball_speed = 5
paddle_acc = 1.06
ball_acc = 1.01
drop_speed = 900
fps = 60
c = 0
timer = pg.time.set_timer(pg.USEREVENT+1, drop_speed)

while game:
    screen.fill(screen_color)
    clock.tick(fps)

    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            game = False

        # keys
        if event.type == pg.KEYDOWN and event.key in [pg.K_LEFT, pg.K_a]:
            items.paddle.x_vel = -paddle_speed
        elif event.type == pg.KEYDOWN and event.key in [pg.K_RIGHT, pg.K_d]:
            items.paddle.x_vel = paddle_speed
        elif event.type == pg.KEYUP:
            items.paddle.x_vel = 0

        # time
        if event.type == pg.USEREVENT+1:
            if c > 0:
                items.add_ball()
            c += 1

            if c % 4 == 0:
                drop_speed -= 80 if drop_speed > 200 else 0
                timer = pg.time.set_timer(pg.USEREVENT + 1, drop_speed)

    items.collision()
    items.update_pos()
    items.show_all()

    pg.display.flip()
    pg.display.update()

# exit
pg.quit()
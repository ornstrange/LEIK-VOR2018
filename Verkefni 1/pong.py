# Örn Óli Strange
# PONG - 17.01.18

import pygame as pg
from random import randint
from rounded import rounded_rect
from text import text_to_screen

"""
Ball: x, y, xVel, yVel, rad, resetFunction, randomStartVel, show, updatePos
Paddle: x, y, w, h, yVel, playerNr, resetFunction, show, updatePos
Items: 2 Paddles, Ball, resetAll, score, printScore, showAll, collision, updatePos
"""

# init stuff
pg.init()
pg.font.init()
clock = pg.time.Clock()
game = True

# screen
screen_width = 800
screen_height = 600
screen = pg.display.set_mode((screen_width, screen_height))
screen_color = (20, 20, 20)

# paddle variables
paddle_width = 20
paddle_height = 160
paddle_speed = 8
paddle_acc = 1.06

# ball variables
ball_speed_range = [3, 4]
ball_max_vel = 8
ball_acc = 1.005
ball_hit_acc = 0.1

fps = 60


class Paddle:
    def __init__(self, x, p):
        self.w = paddle_width
        self.h = paddle_height
        self.x = x
        self.y = screen_height/2 - self.h/2
        self.y_vel = 0
        self.controls = False

        self.player = p

        self.collide_rect = pg.Rect(self.x, self.y, self.w, self.h)

    def show(self):
        pg.draw.rect(screen, (230, 230, 230), self.collide_rect)

    def update_pos(self):
        self.y += self.y_vel if 0 <= self.y + self.y_vel <= screen_height - self.h else 0
        self.y_vel = self.y_vel * paddle_acc
        self.collide_rect = pg.Rect(self.x, self.y, self.w, self.h)

    def reset(self):
        self.y = screen_height / 2 - self.h / 2
        self.y_vel = 0
        self.controls = False
        self.collide_rect = pg.Rect(self.x, self.y, self.w, self.h)


class Ball:
    def __init__(self):
        self.x = int(screen_width/2)
        self.y = int(screen_height/2)
        self.rad = 10
        self.x_vel = 0
        self.y_vel = 0

        self.collide_rect = pg.Rect(self.x - self.rad,
                                    self.y - self.rad,
                                    self.rad * 2,
                                    self.rad * 2)

    def show(self):
        pg.draw.circle(screen, (255, 80, 80), (self.x, self.y), self.rad)

    def update_pos(self):
        # x dir
        self.x += int(self.x_vel)
        self.x_vel = round(self.x_vel * ball_acc, 2)
        self.x_vel = ball_max_vel if self.x_vel >= ball_max_vel else self.x_vel

        # y dir
        self.y += int(self.y_vel)
        self.y_vel = round(self.y_vel * ball_acc, 2)
        self.y_vel = ball_max_vel if self.y_vel >= ball_max_vel else self.y_vel

        # collide_rect
        self.collide_rect = pg.Rect(self.x - self.rad, self.y - self.rad, self.rad * 2, self.rad * 2)

    def random_vel(self):
        self.x_vel = randint(ball_speed_range[0], ball_speed_range[1])
        self.y_vel = randint(ball_speed_range[0], ball_speed_range[1])

    def reset(self):
        self.x, self.y = int(screen_width/2), int(screen_height/2)
        self.x_vel, self.y_vel = 0, 0
        self.collide_rect = pg.Rect(self.x - self.rad, self.y - self.rad, self.rad * 2, self.rad * 2)

    def floor_ceiling(self):
        if not (self.rad/2 <= self.y + self.y_vel <= screen_height - self.rad/2):
            self.y_vel = -self.y_vel

    def left_right(self):
        if self.x <= self.rad / 2:
            return 1
        elif self.x >= screen_width - self.rad/2:
            return 0
        return None


class Items:
    def __init__(self):
        self.ball = Ball()
        self.p1 = Paddle(0, 1)
        self.p2 = Paddle(screen_width-paddle_width, 2)
        self.paddles = [self.p1, self.p2]

        self.start_text = True

        self.score = [0, 0]

    def update_pos(self):
        self.ball.update_pos()
        self.p1.update_pos()
        self.p2.update_pos()

    def reset_all(self):
        self.start_text = True
        self.ball.reset()
        self.p1.reset()
        self.p2.reset()
        self.score = [0, 0]

    def start_game(self):
        self.ball.random_vel()
        self.p1.controls = True
        self.p2.controls = True
        self.start_text = False

    def show_text(self):
        # score
        score = "%d - %d" % (self.score[0], self.score[1])
        text_to_screen(screen, score, screen_width/2 - 45, 16, 32, (230, 230, 230))

        # start text
        if self.start_text:
            text_to_screen(screen, "PRESS SPACE TO START", screen_width / 2 - 94, 64, 16, (180, 180, 180))

    def collision(self):
        for paddle in self.paddles:
            if paddle.collide_rect.colliderect(self.ball.collide_rect):
                self.ball.x_vel = -self.ball.x_vel
                self.ball.x_vel += ball_hit_acc if self.ball.x_vel > 0 else -ball_hit_acc
                self.ball.y_vel += ball_hit_acc if self.ball.y_vel > 0 else -ball_hit_acc

        self.ball.floor_ceiling()

        if self.ball.left_right() in [0, 1]:
            self.score[self.ball.left_right()] += 1
            self.ball.reset()
            self.ball.random_vel()

    def show_all(self):
        self.ball.show()
        self.p1.show()
        self.p2.show()
        self.show_text()


# items
items = Items()

while game:
    screen.fill(screen_color)
    clock.tick(fps)

    for event in pg.event.get():
        # quit
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_q):
            game = False

        # space key
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            items.start_game()

        # keys p1
        if event.type == pg.KEYDOWN and event.key == pg.K_w:
            items.p1.y_vel = -paddle_speed if items.p1.controls else 0
        elif event.type == pg.KEYDOWN and event.key == pg.K_s:
            items.p1.y_vel = paddle_speed if items.p1.controls else 0
        elif event.type == pg.KEYUP and event.key in [pg.K_w, pg.K_s]:
            items.p1.y_vel = 0

        # keys p2
        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            items.p2.y_vel = -paddle_speed if items.p2.controls else 0
        elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            items.p2.y_vel = paddle_speed if items.p2.controls else 0
        elif event.type == pg.KEYUP and event.key in [pg.K_UP, pg.K_DOWN]:
            items.p2.y_vel = 0

    items.collision()
    items.update_pos()
    items.show_all()

    if 7 in items.score:
        items.reset_all()

    pg.display.flip()
    pg.display.update()

# exit
pg.quit()

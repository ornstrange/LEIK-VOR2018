import pygame as pg


def text_to_screen(screen, text, x, y, size=50,
                   color=(200, 000, 000), font_type='fonts/Coco Gothic.ttf'):
    text = str(text)
    font = pg.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))
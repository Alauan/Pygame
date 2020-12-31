import pygame as pg
from time import time
from math import sin
from math import cos

pg.init()


class Ponteiro:
    def __init__(self, pos, degrees, length, width, cor, janela):
        self.pos = pos
        self.degrees = degrees
        self.length = length
        self.width = width
        self.cor = cor
        self.window = janela

    def rotate(self, degrees):
        self.degrees = (self.degrees + degrees) % 360

    def blit(self):
        x = self.pos[0] + int(self.length * sin(self.degrees/57.2958))
        y = self.pos[1] + int(self.length * cos(self.degrees/57.2958))
        pg.draw.line(self.window, self.cor, self.pos, (x, y), self.width)


# janela
window = pg.display.set_mode((200, 200))

# ponteiros
Psegundo = Ponteiro((100, 100), 0, 80, 3, (0, 0, 0), window)
Pminuto = Ponteiro((100, 100), 0, 80, 3, (200, 50, 50), window)
Phora = Ponteiro((100, 100), 0, 50, 3, (0, 0, 0), window)

iniTime = iniFrameTime = time()
taxa = -1
clicou_agora = False
space = False
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            clicou_agora = True
            space = True
        elif event.type == pg.KEYUP and event.key == pg.K_SPACE:
            space = False

# ---------------------- Processamento ------------------------------
    frametime = time() - iniFrameTime
    iniFrameTime = time()
    Time_since_start = int(time() - iniTime)

    if clicou_agora:
        taxa = taxa * -1.05
        clicou_agora = False

    Psegundo.rotate(frametime*6*taxa)
    Pminuto.rotate(frametime*0.1*taxa)
    Phora.rotate(frametime*0.0083333*taxa)


# ---------------------- Blits ---------------------------------------
    window.fill((0, 0, 0))
    pg.draw.circle(window, (90, 120, 200), (100, 100), 90)
    Psegundo.blit()
    Pminuto.blit()
    Phora.blit()
    pg.display.update()

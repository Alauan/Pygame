import pygame as pg
from time import sleep
func = __import__('functions')
clas = __import__('classes')

pg.init()

janela = pg.display.set_mode((700, 400))
mapa = [(0, 3), (3, 3), (3, 0), (6, 0)]
posicao = [5, 6]
keys_pressed = []

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            keys_pressed.append(event.key)
        if event.type == pg.KEYUP:
            keys_pressed.remove(event.key)

    if pg.K_LEFT in keys_pressed:
        posicao[0] -= 0.05
    if pg.K_RIGHT in keys_pressed:
        posicao[0] += 0.05
    if pg.K_UP in keys_pressed:
        posicao[1] -= 0.05
    if pg.K_DOWN in keys_pressed:
        posicao[1] += 0.05

    # ------------------- blits ------------------------

    janela.fill((0, 0, 0))
    janela.blit(func.render(mapa, posicao), (0, 0))

    pg.display.update()
    sleep(0.01)

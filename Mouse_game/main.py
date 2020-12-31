import pygame as pg
from time import time

classes = __import__('Classes1')
Sand = classes.Sand

pg.init()

# janela
width = 400
height = 400
window = pg.display.set_mode((400, 400))

# Cursor: diamond, arrow, broken_x, tri_left
pg.mouse.set_cursor(*pg.cursors.tri_left)

# Sand
cor = (250, 250, 200)
sand = Sand((width//2, height//2), window, cor)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    mousePos = pg.mouse.get_pos()
    clicked = pg.mouse.get_pressed()[0]

    if clicked:
        ini_time = time()
        sand.pour((mousePos[0] // 2, mousePos[1]//2))
        for i in range(1, 1):
            sand.pour((mousePos[0] // 2 + i, mousePos[1]//2))
            sand.pour((mousePos[0] // 2 - i, mousePos[1]//2))
        print(f'Por a areia: {time()-ini_time:.4f}')

    ini_time = time()
    sand.move()
    print(f'Mover a areia: {time() - ini_time:.4f}')

    # ------------------------------ Blits --------------------------
    window.fill((0, 0, 0))
    sand.blit()
    pg.display.update()

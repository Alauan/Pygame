import pygame as pg
from time import time

pg.init()

# janela
window = pg.display.set_mode((500, 150))

# cores
vermelho = (250, 120, 120)
branco = (255, 255, 255)
cinza = (100, 100, 100)
cinza_claro = (150, 150, 150)
preto = (0, 0, 0)

# morse information
dah_time = 0.4
translate = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i',
             '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q',
             '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y',
             '--..': 'z'}

# espaço
duration = 0
start_time = time()
pressed = False
action = False

# caracteres
code = ''  # código (dits e dots de uma combinação)
frase = ''
frase_surface = pg.Surface((0, 0))
code_surface = pg.Surface((0, 0))

# fonte
fonte1 = pg.font.SysFont('Tw Cen MT', 35)

running = True
while running:
    # -------------------------------- Inputs ------------------------------------
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            pressed = True
            action = True
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            pressed = False
            action = True

    # --------------------------------- Processamento -----------------------------
    duration = time() - start_time
    if action:
        if not pressed:  # Se acabou de soltar a barra
            if duration > dah_time:  # escolhe se é dit ou dah
                code += '-'
            else:
                code += '.'

            code_surface = fonte1.render(code, True, branco)
            try:
                translate[code]
            except KeyError:
                code_surface = fonte1.render(code, True, vermelho)

        start_time = time()
        duration = 0

    if duration > dah_time and not pressed:
        try:
            frase += translate[code]
            frase_surface = fonte1.render(frase, True, branco)
            code = ''
        except KeyError:
            code = ''
            pass
        code_surface = pg.Surface((0, 0))

    if duration > dah_time * 2.3 and frase and frase[-1] != ' ':
        frase += ' '

    action = False

    if pressed:
        bar_color = branco
        bar_size = duration * 100 / dah_time
    else:
        bar_color = preto
        bar_size = duration * 100 / (dah_time * 2.3)

    if bar_size > 100:
        bar_size = 100

    # --------------------------------- Blits -------------------------------------
    window.fill(preto)
    window.blit(frase_surface, (250-frase_surface.get_width()//2, 100))
    window.blit(code_surface, (250-code_surface.get_width()//2, 45))
    window.fill(cinza, ((200, 18), (100, 4)))
    window.fill(cinza_claro, ((200, 18), (44, 4)))
    pg.draw.line(window, bar_color, (200, 19), (200+int(bar_size), 19), 4)
    pg.display.update()

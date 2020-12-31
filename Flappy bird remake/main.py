import pygame as pg
from time import time
from random import randint, choice

pg.init()

# cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# janela e background
janelaHeight = 800
janelaWidth = 600
janela = pg.display.set_mode((janelaWidth, janelaHeight))
background = pg.image.load('data/background.png')
background = pg.transform.scale(background, (600, 800)).convert_alpha()

# fonte e score
fonte1 = pg.font.SysFont('Unispace Negrito', 140)
score = 0
scoreImg = fonte1.render(str(score), True, branco)

# Canudos e canos
distancia_H = 350
distancia_V = 250
canoHeight = 720
canoWidth = 80
cano_v = - 200

canoImg = pg.image.load('data/cano.png')
canoImg = pg.transform.scale(canoImg, (canoWidth, canoHeight)).convert_alpha()
canudoImg = pg.image.load('data/canudo.png')
canudoImg = pg.transform.scale(canudoImg, (canoWidth, canoHeight)).convert_alpha()

# passaro
bird = pg.image.load('data/bird.png')
bird = pg.transform.scale(bird, (90, 90))


class Objeto:
    def __init__(self, imagem, coordenadas=(0, 0), orientacao=0, v_x=0, v_y=0, gravidade=False):
        self.imagem = imagem
        self.x = coordenadas[0]
        self.y = coordenadas[1]
        self.v_x = v_x
        self.v_y = v_y
        self.orientacao = orientacao

        self.gravidade = 1500 if gravidade else 0

    def pular(self):
        self.v_y = -600

    def physics(self, tempo):
        self.v_y += self.gravidade * tempo
        self.y += self.v_y * tempo
        self.x += self.v_x * tempo

    def blit(self):
        imagem = pg.transform.rotate(self.imagem, self.orientacao)
        janela.blit(imagem, (int(self.x), int(self.y)))


iniTempo = time()
jaime = Objeto(bird, (70, 300), gravidade=True)
canudo = list()
for i in range(3):
    Imagem = choice((canoImg, canudoImg))
    altura_cano = randint(300, 700)
    canudo.append((Objeto(Imagem, (600 + i * distancia_H, altura_cano), v_x=cano_v),
                   Objeto(Imagem, (600 + i * distancia_H, altura_cano - 720 - distancia_V), 180, cano_v)))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                jaime.pular()

    # cálculos de tempo
    frameTime = time() - iniTempo
    iniTempo = time()

    # Se o cano ficou pra trás
    if canudo[0][0].x < -80:
        canudo.pop(0)
        Imagem = choice((canoImg, canudoImg))
        altura_cano = randint(300, 700)
        canudo.append((Objeto(Imagem, (canudo[-1][0].x + distancia_H, altura_cano), v_x=cano_v),
                       Objeto(Imagem, (canudo[-1][0].x + distancia_H, altura_cano - 720 - 200), 180, cano_v)))

    # se passou pelo cano
    for i in canudo:
        if i[0].x > jaime.x > i[0].x + i[0].v_x * frameTime:
            score += 1
            scoreImg = fonte1.render(str(score), True, branco)

    # Se bateu no canudo
    for i in canudo:
        if i[0].x < jaime.x + 60 < i[0].x + canoWidth and i[0].y < jaime.y + 60:
            running = False
        if i[1].x < jaime.x + 60 < i[1].x + canoWidth and i[1].y + canoHeight > jaime.y + 21:
            running = False

    # se bateu no chão ou no teto
    if jaime.y + 60 > janelaHeight or jaime.y + 21 < 0:
        running = False

    jaime.physics(frameTime)
    jaime.orientacao = -jaime.v_y // 20

    # ------------------------------------- Blits --------------------------------------------

    janela.blit(background, (0, 0))
    # canos
    for i in canudo:
        for b in i:
            b.physics(frameTime)
            b.blit()

    jaime.blit()
    janela.blit(scoreImg, (janelaWidth // 2 - 70, 80))

    pg.display.update()


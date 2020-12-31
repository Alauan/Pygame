import pygame as pg
import numpy as np
from random import choice

pg.init()

# janela
janela = pg.display.set_mode((200, 300))


def ao_redor(linha, coluna):
    return ((linha-1, coluna-1), (linha, coluna-1), (linha+1, coluna-1), (linha-1, coluna),
            (linha+1, coluna), (linha-1, coluna+1), (linha, coluna+1), (linha+1, coluna+1))


class Campo:
    def __init__(self, dimensoes=(15, 15), pos_inicial=(0, 0), n_de_bombas=0):
        # informações diversas
        self.dimensoes = dimensoes
        self.Bsize = 30
        self.bombaQtd = n_de_bombas
        janela = pg.display.set_mode((dimensoes[1] * self.Bsize, dimensoes[0] * self.Bsize))

        # criação do mapa
        self.mapa = np.ones((self.dimensoes[0], self.dimensoes[1]), dtype='int')
        self.mapa_real = np.zeros((self.dimensoes[0], self.dimensoes[1]), dtype='int')

        remove = list()
        for y in range(pos_inicial[0]-3, pos_inicial[0]+3):
            for x in range(pos_inicial[1]-3, pos_inicial[1]+3):
                remove.append((x, y))
        for c in range(self.bombaQtd):
            linha = choice(range(self.dimensoes[0]))
            coluna = choice(range(self.dimensoes[1]))
            while (linha, coluna) in remove:
                linha = choice(range(self.dimensoes[0]))
                coluna = choice(range(self.dimensoes[1]))
            remove.append((linha, coluna))
            self.mapa_real[linha][coluna] = 6
            for z in ao_redor(linha, coluna):
                if 0 <= z[0] <= self.dimensoes[0]-1 and 0 <= z[1] <= self.dimensoes[1]-1 \
                   and self.mapa_real[z[0], z[1]] != 6:
                    self.mapa_real[z[0], z[1]] += 1
        # imagens
        vazio_img = pg.image.load('data/vazio.png')
        um_img = pg.image.load('data/1.png')
        dois_img = pg.image.load('data/2.png')
        tres_img = pg.image.load('data/3.png')
        quatro_img = pg.image.load('data/4.png')
        cinco_img = pg.image.load('data/5.png')
        bomba_img = pg.image.load('data/bomba.png')
        bandeira_img = pg.image.load('data/bandeira.png')
        espaco_img = pg.image.load('data/espaco.png')
        explodiu_img = pg.image.load('data/explodiu.png')
        self.elementos = (vazio_img, um_img, dois_img, tres_img, quatro_img,
                          cinco_img, bomba_img, bandeira_img, espaco_img, explodiu_img)

    def blit(self, surface):
        for linha, objeto in enumerate(self.mapa):
            for coluna, valor in enumerate(objeto):
                if valor == 2:
                    surface.blit(self.elementos[self.mapa_real[linha, coluna]],
                                 (coluna * self.Bsize, linha * self.Bsize))
                elif valor == 0:
                    surface.blit(self.elementos[7], (coluna * self.Bsize, linha * self.Bsize))
                else:
                    surface.blit(self.elementos[8], (coluna * self.Bsize, linha * self.Bsize))


def jogo(dimensoes, n_bombas):
    campo = Campo(dimensoes)
    primeira_jogada = True
    running = True
    while running:
        # ---------------------------------------- Input ----------------------------------------
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if primeira_jogada:
                        campo = Campo(dimensoes, (event.pos[0] // campo.Bsize, event.pos[1] // campo.Bsize), n_bombas)
                        primeira_jogada = False
                    bt = 'esq'
                elif event.button == 3:
                    bt = 'dir'
                else:
                    bt = 'meio'
                pos = (event.pos[0] // campo.Bsize, event.pos[1] // campo.Bsize)

        # ------------------------------------------ Processamento --------------------------------
                if bt == 'esq':     # tentativas
                    if campo.mapa[pos[1], pos[0]] < 2:      # se apertou em um campo coberto
                        campo.mapa[pos[1], pos[0]] += 1

                    if 1 <= campo.mapa_real[pos[1], pos[0]] <= 5:       # apertou em um número?
                        cont = 0

                        for i in ao_redor(pos[1], pos[0]):
                            if 0 <= i[0] <= campo.dimensoes[0] - 1 and 0 <= i[1] <= campo.dimensoes[1] - 1:
                                if campo.mapa[i[0], i[1]] == 0:
                                    cont += 1
                        if cont == campo.mapa_real[pos[1], pos[0]]:     # a quantidade de bandeiras é igual ao número?
                            for i in ao_redor(pos[1], pos[0]):
                                if 0 <= i[0] <= campo.dimensoes[0] - 1 and 0 <= i[1] <= campo.dimensoes[1] - 1:
                                    if campo.mapa[i[0], i[1]] == 1:
                                        campo.mapa[i[0], i[1]] = 2

                    # se for vazio
                    for b in range(max(campo.dimensoes)):
                        for row, lista in enumerate(campo.mapa):
                            for col, value in enumerate(lista):
                                if campo.mapa_real[row, col] == 0 and campo.mapa[row, col] == 2:
                                    for i in ao_redor(row, col):
                                        if 0 <= i[0] <= campo.dimensoes[0] - 1 \
                                           and 0 <= i[1] <= campo.dimensoes[1] - 1:
                                            campo.mapa[i[0], i[1]] = 2
                    # se tiver bomba
                    for row, lista in enumerate(campo.mapa):
                        for col, value in enumerate(lista):
                            if value == 2 and campo.mapa_real[row, col] == 6:
                                campo.mapa = np.full_like(campo.mapa, 2)
                                campo.mapa_real[row, col] = 9

                if bt == 'dir':     # bandeiras
                    if campo.mapa[pos[1], pos[0]] == 1:
                        campo.mapa[pos[1], pos[0]] = 0
                    elif campo.mapa[pos[1], pos[0]] == 0:
                        campo.mapa[pos[1], pos[0]] = 1

        # ------------------------------------------ Blits ----------------------------------------
        campo.blit(janela)
        pg.display.update()


def menu():
    running = True
    fonte = pg.font.SysFont('Unispace Negrito', 60)
    dificuldade = ('Fácil', 'Médio', 'Difícil')
    dificuldade_surface = list()
    for i in dificuldade:
        dificuldade_surface.append(fonte.render(i, True, (0, 0, 0)))

    while running:
        # ----------------------------------------- Input ----------------------------------------
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = event.pos
        # ----------------------------------------- Processamento --------------------------------
                    if pos[1] // 100 == 0:
                        return (15, 15), 20
                    elif pos[1] // 100 == 1:
                        return (25, 30), 80
                    elif pos[1] // 100 == 2:
                        return (25, 50), 150
        # ----------------------------------------- Blits ----------------------------------------
        janela.fill((255, 255, 255))
        for i in range(3):
            pg.draw.rect(janela, (0, 0, 0), ((10, 10 + i * 100), (180, 80)), 4)
            janela.blit(dificuldade_surface[i], (30, 30 + i * 100))
        pg.display.update()


parametros = menu()
jogo(parametros[0], parametros[1])

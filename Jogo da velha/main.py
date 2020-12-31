import pygame as pg
import numpy as np
import pickle
from time import sleep
ClassAI = __import__('ClassAI')
AI = ClassAI.AI


# ------------------------------- AI and game rules section -----------------------------
# Importando a memória e criando as AIs
pickle_in = open('memoryFirst.pickle', 'rb')
memory = pickle.load(pickle_in)
AIFirst = AI(memory)

pickle_in = open('memorySecond.pickle', 'rb')
memory = pickle.load(pickle_in)
AISecond = AI(memory)


# regras do jogo
def result(space):
    for row in space:
        if all(b == 1 for b in row):
            return 'p1'
        if all(b == 2 for b in row):
            return 'p2'
    for col in np.rot90(space):
        if all(b == 1 for b in col):
            return 'p1'
        if all(b == 2 for b in col):
            return 'p2'

    if space[0][0] == space[1][1] == space[2][2] == 1 or \
       space[0][2] == space[1][1] == space[2][0] == 1:
        return 'p1'

    if space[0][0] == space[1][1] == space[2][2] == 2 or \
       space[0][2] == space[1][1] == space[2][0] == 2:
        return 'p2'

    if all(all(b > 0 for b in row) for row in space):
        return 'draw'
# ----------------------------- pygame section --------------------------------------


pg.init()

# janela
janela = pg.display.set_mode((300, 300))
icone = pg.image.load('icone.png')
pg.display.set_icon(icone)
pg.display.set_caption('Jogo da Velha')

# cores
preto = (0, 0, 0)
branco = (255, 255, 255)

# fontes
fonte = pg.font.SysFont('Agency FB', 70)


# blit do tabuleiro
def blit_map(surface):
    pg.draw.line(surface, branco, (100, 0), (100, 300), 3)
    pg.draw.line(surface, branco, (200, 0), (200, 300), 3)
    pg.draw.line(surface, branco, (0, 100), (300, 100), 3)
    pg.draw.line(surface, branco, (0, 200), (300, 200), 3)


# blit do x e o
def blit_simbols(mapa, surface):
    for row, lista in enumerate(mapa):
        for col, valor in enumerate(lista):
            if valor == 1:
                pg.draw.line(surface, branco, (col * 100 + 20, row * 100 + 20), (col * 100 + 80, row * 100 + 80), 4)
                pg.draw.line(surface, branco, (col * 100 + 20, row * 100 + 80), (col * 100 + 80, row * 100 + 20), 4)
            if valor == 2:
                pg.draw.circle(surface, branco, (col * 100 + 50, row * 100 + 50), 40, 2)


# animação de vitória
def acabou(tabuleiro):
    coord1 = (0, 0)
    coord2 = (0, 0)

    for row, lista in enumerate(tabuleiro):
        if all(b > 0 for b in lista):
            coord1 = (30, row * 100 + 50)
            coord2 = (270, row * 100 + 50)
    for col, lista in enumerate(np.rot90(tabuleiro, -1)):
        if all(b > 0 for b in lista):
            coord1 = (col * 100 + 50, 30)
            coord2 = (col * 100 + 50, 270)

    if tabuleiro[0][0] == tabuleiro[1][1] == tabuleiro[2][2] > 0:
        coord1 = (30, 30)
        coord2 = (270, 270)

    if tabuleiro[0][2] == tabuleiro[1][1] == tabuleiro[2][0] > 0:
        coord1 = (270, 30)
        coord2 = (30, 270)

    pg.draw.line(janela, (240, 150, 150), coord1, coord2, 3)
    pg.display.update()
    sleep(1)


class Botao:
    def __init__(self, coord, dimentions, texto):
        self.texto = texto
        self.texto_branco = fonte.render(texto, True, branco)
        self.texto_preto = fonte.render(texto, True, preto)
        self.x = coord[0]
        self.y = coord[1]
        self.width = dimentions[0]
        self.height = dimentions[1]

    def esta_em_cima(self, cursor_position):
        if self.x < cursor_position[0] < self.x + self.width and self.y < cursor_position[1] < self.y + self.height:
            return True
        else:
            return False

    def blit(self, cursor_position):
        width = self.texto_preto.get_width()
        height = self.texto_preto.get_height()
        if self.esta_em_cima(cursor_position):
            pg.draw.rect(janela, branco, ((self.x, self.y), (self.width, self.height)))
            janela.blit(self.texto_preto, (self.x + (self.width - width)//2, self.y + (self.height - height)//2))
        else:
            pg.draw.rect(janela, branco, ((self.x, self.y), (self.width, self.height)), 3)
            janela.blit(self.texto_branco, (self.x + (self.width - width)//2, self.y + (self.height - height)//2))


class Menu:
    def __init__(self, botoes):
        self.n_botoes = len(botoes)
        for i in botoes:
            i.height = (290 - len(botoes) * 10) // len(botoes)
        self.botoes = botoes

    def run(self):
        posicao = tuple()
        click = False
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif evento.type == pg.MOUSEMOTION:
                    posicao = evento.pos
                if evento.type == pg.MOUSEBUTTONDOWN:
                    click = True

            if posicao:
                if click:
                    for i in self.botoes:
                        if i.esta_em_cima(posicao):
                            janela.fill(preto)
                            return i.texto

                janela.fill(preto)
                for i in self.botoes:
                    i.blit(posicao)
                pg.display.update()


class Jogo:
    def __init__(self, ai):
        self.AI = ai

    @staticmethod
    def player_play(possibilidades):
        position = tuple()
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    exit()
                if evento.type == pg.MOUSEBUTTONDOWN:
                    position = evento.pos
            if position:
                escolha = (position[1] // 100, position[0] // 100)
                if escolha in possibilidades:
                    return escolha

    def ai_play(self, tabuleiro, possibilidades, ai_first):
        if ai_first:
            escolha = self.AI[0].escolher(tabuleiro, possibilidades)
            self.AI[0].tab(tabuleiro)
        else:
            escolha = self.AI[1].escolher(tabuleiro, possibilidades)
            self.AI[1].tab(tabuleiro)
        return escolha

    def run(self, pvp, ai_first=False):

        janela.fill(preto)
        blit_map(janela)
        pg.display.update()

        tabuleiro = [[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]]

        possible = list()
        for a in range(3):
            for c in range(3):
                possible.append((a, c))

        while True:
            # jogador 1
            if pvp or not ai_first:
                escolha = self.player_play(possible)

            else:
                escolha = self.ai_play(tabuleiro, possible, True)

            tabuleiro[escolha[0]][escolha[1]] = 1  # coloca a escolha no tabuleiro
            possible.remove(escolha)

            janela.fill(preto)
            blit_map(janela)
            blit_simbols(tabuleiro, janela)
            pg.display.update()

            if result(tabuleiro) is not None:
                break

            # jogador 2
            if pvp or ai_first:
                escolha = self.player_play(possible)

            else:
                escolha = self.ai_play(tabuleiro, possible, False)

            tabuleiro[escolha[0]][escolha[1]] = 2  # coloca a escolha no tabuleiro
            possible.remove(escolha)

            janela.fill(preto)
            blit_map(janela)
            blit_simbols(tabuleiro, janela)
            pg.display.update()

            if result(tabuleiro) is not None:
                break

        acabou(tabuleiro)


# menu principal
bt_pvp = Botao((10, 10), (280, 130), 'PvP')
bt_pvai = Botao((10, 160), (280, 130), 'PvAI')
menu_principal = Menu((bt_pvp, bt_pvai))

# menu ai
bt_start_player = Botao((10, 10), (280, 130), 'Eu começo')
bt_start_ai = Botao((10, 160), (280, 130), 'AI começa')
menuAi = Menu((bt_start_player, bt_start_ai))

# jogo
jogo = Jogo((AIFirst, AISecond))

# ------------------------------------------ running -------------------------------------------------
running = True
while running:
    if menu_principal.run() == 'PvP':
        jogo.run(True)
    else:
        if menuAi.run() == 'Eu começo':
            jogo.run(False, False)
        else:
            jogo.run(False, True)

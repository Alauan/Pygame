import pygame
from time import sleep
from random import randint, getrandbits

pygame.init()
frames = 0

# ------------------------------------------- DEFINIÇÃO DE OBJETOS -----------------------------------------------------
# janela
tela = pygame.display.set_mode((795, 600))
pygame.display.set_caption('Jogo da cobrosa')
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

# cobra
cobraImg1 = pygame.image.load('corpodacobrinha1.png')
cobraImg2 = pygame.image.load('corpodacobrinha2.png')
cobraImg3 = pygame.image.load('corpodacobrinha3.png')
cobra = [[3, 15], [4, 15], [5, 15]]

# lingua
linguaCimImg = pygame.image.load('linguaCim.png')
linguaDirImg = pygame.image.load('linguaDir.png')
linguaBaiImg = pygame.image.load('linguaBai.png')
linguaEsqImg = pygame.image.load('linguaEsq.png')
islingua = False
animalingua = False

# comida
comidaImg = pygame.image.load('fruta.png')
comidaX = randint(0, 52) * 15
comidaY = randint(0, 39) * 15

# parede
paredeImg = pygame.image.load('parede.png')
parede = list()

# escudo
escudoImg = pygame.image.load('escudo.png')
escudoX = -1
escudoY = -1
temEscudo = False

# fontes
font = pygame.font.Font('freesansbold.ttf', 32)
font1 = pygame.font.Font('freesansbold.ttf', 16)

# score
scoreValue = 0
highScoreValue = 0
scoreX = 10
scoreY = 10
highScoreX = 700
highScoreY = 10

# game over
goverX = 300
goverY = 250

direcao = 'right'
direcaoframe = list()
direcaoframe.append('right')
# ---------------------------------------------- FUNÇÕES ---------------------------------------------------------------


def blitCobra():
    if temEscudo is False:
        for i, v in enumerate(cobra):
            if i % 2:
                tela.blit(cobraImg1, (v[0] * 15, v[1] * 15))
            else:
                tela.blit(cobraImg2, (v[0] * 15, v[1] * 15))
    else:
        for i in cobra:
            tela.blit(cobraImg3, (i[0] * 15, i[1] * 15))

def blit_lingua(x, y, dire):
    if dire == 'up':  # Cima
        tela.blit(linguaCimImg, (x + 5, y + 10))
    if dire == 'right':  # Direita
        tela.blit(linguaDirImg, (x + 15, y + 5))
    if dire == 'down':  # Baixo
        tela.blit(linguaBaiImg, (x + 5, y + 15))
    if dire == 'left':  # Esquerda
        tela.blit(linguaEsqImg, (x - 5, y + 5))


def blitComida(x, y):
    tela.blit(comidaImg, (x, y - 8))


def blitScore(xscore, yscore, xhigh, yhigh):
    score = font.render(str(scoreValue), True, (0, 0, 0))
    tela.blit(score, (xscore, yscore))
    high_score = font.render('HI: ' + str(highScoreValue), True, (0, 0, 0))
    tela.blit(high_score, (xhigh, yhigh))


def blit_parede(x, y):
    tela.blit(paredeImg, (x, y))


def blit_gameover():
    gover = font.render('Game Over', True, (0, 0, 0))
    tela.blit(gover, (goverX, goverY))
    continuar = font1.render('pressione qualquer tecla para continuar', True, (0, 0, 0))
    tela.blit(continuar, (goverX - 60, goverY + 50))


def blit_escudo(x, y):
    tela.blit(escudoImg, (x, y))


# ----------------------------------------------------- MAIN LOOPS -----------------------------------------------------
jogando = True
running = True
while running:
    while jogando:
        tela.fill((255, 255, 255))

# ----------------------------------------------- LEITURA E MOVIMENTO --------------------------------------------------
        event = pygame.event.get()
        if event:
            event = event[0]
            if event.type == pygame.QUIT:
                jogando = False
                running = False

            elif event.type == pygame.KEYDOWN:
                if direcao != 'right' and event.key == pygame.K_LEFT:
                    direcao = 'left'
                elif direcao != 'left' and event.key == pygame.K_RIGHT:
                    direcao = 'right'
                elif direcao != 'down' and event.key == pygame.K_UP:
                    direcao = 'up'
                elif direcao != 'up' and event.key == pygame.K_DOWN:
                    direcao = 'down'
                direcaoframe.append(direcao)

        if frames % 4 == 0:
            if len(direcaoframe) > 1:
                direcaoframe.pop(0)
            if direcaoframe[0] == 'right':
                cobra.append([(cobra[-1][0] + 1) % 53, cobra[-1][1] % 40])
            elif direcaoframe[0] == 'left':
                cobra.append([(cobra[-1][0] - 1) % 53, cobra[-1][1] % 40])
            elif direcaoframe[0] == 'up':
                cobra.append([cobra[-1][0] % 53, (cobra[-1][1] - 1) % 40])
            elif direcaoframe[0] == 'down':
                cobra.append([cobra[-1][0] % 53, (cobra[-1][1] + 1) % 40])

# ---------------------------------------------- VERIFICAÇÕES ----------------------------------------------------------
            # bateu em si mesma ou na parede?
            for i in cobra[0: -2]:
                if cobra[-1] == i:
                    jogando = False
            for i in parede:
                if cobra[-1] == i:
                    if temEscudo:
                        parede.remove(i)
                        temEscudo = False
                    else:
                        jogando = False

            # comeu a comida?
            if cobra[-1][0] * 15 != comidaX or cobra[-1][1] * 15 != comidaY:
                cobra.pop(0)
            else:
                # criação da parede
                parede.append(cobra[0])
                comidaX = randint(0, 52) * 15
                comidaY = randint(0, 39) * 15
                while [comidaX, comidaY] in parede or [comidaX / 15, comidaY / 15] in cobra:
                    comidaX = randint(0, 52) * 15
                    comidaY = randint(0, 39) * 15

                scoreValue += 1

            # Pegou um escudo?
            if cobra[-1] == [escudoX / 15, escudoY / 15]:
                temEscudo = True
                escudoX = -1

            # vai ter linguinha?
            if islingua:
                if bool(getrandbits(1)):
                    islingua = True
                else:
                    islingua = False
            else:
                if randint(0, 20) == 0:
                    islingua = True
                else:
                    islingua = False

            # vai ter escudo?
            if scoreValue % 15 == 0 and temEscudo is False and escudoX == -1 and scoreValue != 0:
                escudoX = randint(0, 52) * 15
                escudoY = randint(0, 39) * 15
                while [escudoX, escudoY] in parede or [escudoX / 15, escudoY / 15] in cobra:
                    escudoX = randint(0, 52) * 15
                    escudoY = randint(0, 39) * 15

# ----------------------------------------------- BLITS ----------------------------------------------------------------
        if islingua:
            if animalingua:
                blit_lingua(cobra[-1][0] * 15, cobra[-1][1] * 15, direcaoframe[0])
                animalingua = False
            else:
                animalingua = True

        if escudoX > -1:
            blit_escudo(escudoX, escudoY)

        blitComida(comidaX, comidaY)

        blitCobra()

        blitScore(scoreX, scoreY, highScoreX, highScoreY)

        if parede:
            for i in parede:
                blit_parede(i[0] * 15, i[1] * 15)

        pygame.display.update()

        sleep(0.025 / (scoreValue * 0.04 + 1))
        frames += 1

# ------------------------------------------ TELA FINAL ----------------------------------------------------------------
    blit_gameover()
    pygame.display.update()
    if highScoreValue < scoreValue:
        highScoreValue = scoreValue
    sleep(0.8)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            cobra = [[3, 15], [4, 15], [5, 15]]
            scoreValue = 0
            direcao = 'right'
            direcaoframe = ['right']
            parede.clear()
            jogando = True
            temEscudo = False
            escudoX = -1


import pygame
from random import choice
from time import sleep

pygame.init()

# janela
janela = pygame.display.set_mode((1000, 700))

# fontes
fonte1 = pygame.font.SysFont('Agency FB', 40)
fonte2 = pygame.font.SysFont('Agency FB', 70)

# cores
preto = (0, 0, 0)
azul = (100, 100, 240)
branco = (240, 253, 255)

# forca
forca = pygame.image.load('forca.png')

# personagem
cabeca = pygame.image.load('cabeca.png')
corpo = pygame.image.load('corpo.png')
bracoD = pygame.image.load('Bdireito.png')
bracoE = pygame.image.load('Besquerdo.png')
pernaD = pygame.image.load('Pdireita.png')
pernaE = pygame.image.load('Pesquerda.png')
personagemImg = [cabeca, corpo, bracoD, bracoE, pernaD, pernaE]


def reiniciar(perdeu=False):
    global pontos, pontosImg, inputs, palavraImg, partes, categoria, dica, palavras, lista, palavra
    if perdeu:
        pontos = 0
    else:
        pontos += 1
    pontosImg = fonte1.render(f'Pontos: {pontos}', True, preto)
    inputs = '- '
    palavraImg = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    partes = 0
    # categoria
    categoria = choice(('Animal', 'Objeto', 'Lugar'))
    dica = fonte2.render(categoria, True, (0, 0, 0))
    # palavras
    palavras = open(f'{categoria}.txt', 'r', encoding='utf8')
    lista = palavras.readlines()
    palavra = choice(lista).lower().strip()


venceu = False
reiniciar(True)
running = True
while running:

    # ------------------------------------- INPUT -----------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            tecla = event.unicode.lower()
            if tecla.isalpha() and tecla not in inputs:

                # ------------------------------------ PROCESSOS ---------------------------------------------
                inputs += tecla + ' '
                inputsImg = fonte1.render(inputs[2:], True, azul)
                if tecla in palavra:
                    for i, letra in enumerate(palavra):
                        if tecla == letra:
                            palavraImg[i] = fonte1.render(letra, True, preto)
                    for i in palavra:
                        if i not in inputs:
                            venceu = False
                            break
                        else:
                            venceu = True
                    if venceu:
                        reiniciar()

                else:
                    partes += 1

    # ------------------------------------ BLITS -------------------------------------------------
    janela.fill(branco)

    # Linhas e palavra
    for i, letra in enumerate(palavra):
        if letra == '-':
            pygame.draw.rect(janela, preto, ((20 + 50 * i, 580), (20, 4)))
        elif letra != ' ':
            pygame.draw.rect(janela, preto, ((10 + 50 * i, 600), (40, 5)))

    for i, letra in enumerate(palavraImg):
        if letra:
            janela.blit(letra, (20 + 50 * i, 550))
    if len(inputs) > 2:
        janela.blit(inputsImg, (50, 630))

    # forca
    janela.blit(forca, (100, 100))
    for i in range(partes):
        janela.blit(personagemImg[i], (100, 100))

    # interface
    janela.blit(pontosImg, (500, 380))
    janela.blit(dica, (500, 300))

    if partes == 6:
        janela.fill(branco)
        janela.blit(fonte1.render(f'A palavra era {palavra}', True, preto), (100, 300))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                reiniciar(True)

    pygame.display.update()
    if venceu:
        sleep(1)

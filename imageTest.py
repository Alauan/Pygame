import pygame
import numpy as np
from PIL import Image

# janela
janela = pygame.display.set_mode((1000, 700))

fundo = pygame.image.load('Data/papel de parede.jpg')

imagem = Image.open('Data/Data/Mascara.png')
array = np.array(imagem)
array = 255 - array
print(array.shape)
img = Image.fromarray(array)
img.show()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    janela.blit(fundo, (0, 0))

    pygame.display.update()
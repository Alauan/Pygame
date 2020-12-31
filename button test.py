import pygame

# janela
janela = pygame.display.set_mode((1000, 700))

cont = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and (500 >= event.pos[0] >= 300 and 500 >= event.pos[1] >= 300):
            cont += 1
            print(cont)
            print(event)

        janela.fill((0, 0, 0))
        pygame.draw.rect(janela, (255, 255, 255), ((300, 300), (200, 200)))


    pygame.display.update()
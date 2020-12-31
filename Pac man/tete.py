import pygame as pg
from time import sleep
from math import sin, radians


class PacMan:
    def __init__(self, screen):
        self.screen: pg.Surface = screen
        self.x = 50
        self.y = 50
        self.move = self.right
        self.opening = True
        self.mouth_angle = 0

    def frame(self):
        self.move()
        self.change_direction()
        self.mouth_angle += 1 if self.opening else -1
        if not 0 < self.mouth_angle < 30:
            self.opening = not self.opening

    def blit(self):
        pg.draw.circle(self.screen, (255, 255, 0), (self.x, self.y), 20)
        displace = int(sin(radians(self.mouth_angle))*20)

        dic = {self.right: [(self.x+20, self.y+displace), (self.x+20, self.y-displace)],
               self.left: [(self.x-20, self.y+displace), (self.x-20, self.y-displace)],
               self.up: [(self.x+displace, self.y-20), (self.x-displace, self.y-20)],
               self.down: [(self.x+displace, self.y+20), (self.x-displace, self.y+20)]}

        points = [(self.x, self.y)] + dic.get(self.move)

        pg.draw.polygon(self.screen, (0, 0, 0), points)

    # Moves

    def right(self):
        self.x += 1

    def left(self):
        self.x -= 1

    def down(self):
        self.y += 1

    def up(self):
        self.y -= 1

    @staticmethod
    def events_handler():
        valid = [event for event in pg.event.get()
                 if event.type == pg.KEYDOWN and event.key in (pg.K_DOWN, pg.K_UP, pg.K_LEFT, pg.K_RIGHT)]
        return valid[-1].key if valid else None

    def change_direction(self):
        dic = {pg.K_RIGHT: self.right,
               pg.K_LEFT: self.left,
               pg.K_UP: self.up,
               pg.K_DOWN: self.down}
        self.move = dic.get(self.events_handler()) or self.move


tela = pg.display.set_mode((800, 600))
pc = PacMan(tela)
while True:
    tela.fill((0, 0, 0))
    pc.frame()
    pc.blit()
    pg.display.update()
    sleep(0.01)

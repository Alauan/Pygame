import pygame as pg
import sys
from time import sleep
import winsound


class Cases:
    def __init__(self):
        self.blue = 50, 70, 255
        self.red = 255, 70, 50
        self.green = 40, 255, 40
        self.length = 30
        self.diag = self.length // 1.4

    def __call__(self, num, point):
        return getattr(self, 'case_' + str(num))(point)

    def case_0(self, point):
        return (point[0], point[1] - self.length), (255, 255, 255)

    def case_1(self, point):
        return (point[0] + self.diag, point[1] - self.diag), self.blue

    def case_2(self, point):
        return (point[0] + self.length, point[1]), self.blue

    def case_3(self, point):
        return (point[0] + self.diag, point[1] + self.diag), self.blue

    def case_4(self, point):
        return self.case_1(point)[0], self.green

    def case_5(self, point):
        return self.case_2(point)[0], self.green

    def case_6(self, point):
        return self.case_3(point)[0], self.green

    def case_7(self, point):
        return self.case_1(point)[0], self.red

    def case_8(self, point):
        return self.case_2(point)[0], self.red

    def case_9(self, point):
        return self.case_3(point)[0], self.red


cases = Cases()

pg.init()

screen = pg.display.set_mode((600, 600))


def sair():
    pg.quit()
    sys.exit()


coord = 100, 500
keys = []
while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sair()
        if event.type == pg.KEYDOWN:
            if event.unicode == '\r':
                for dig in keys:
                    instructions = cases(dig, coord)
                    color = instructions[1]
                    pg.draw.line(screen, color, coord, instructions[0], 3)
                    coord = instructions[0]

                pg.display.update()
            else:
                keys.append(event.unicode)







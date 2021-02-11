import pygame as pg
import sys
from time import sleep
import winsound
from random import randrange


class Cases:
    def __init__(self):
        self.C = 261
        self.D = 293
        self.E = 329
        self.G = 392
        self.A = 440
        self.notetime = 500

    def __call__(self, num):
        return getattr(self, 'case_' + str(num))()

    def case_0(self):
        winsound.Beep(self.C, self.notetime)

    def case_1(self):
        winsound.Beep(self.D, self.notetime)

    def case_2(self):
        winsound.Beep(self.E, self.notetime)

    def case_3(self):
        winsound.Beep(self.G, self.notetime)

    def case_4(self):
        winsound.Beep(self.A, self.notetime)

    def case_5(self):
        for _ in range(2):
            winsound.Beep(self.C, self.notetime//4)
            sleep(self.notetime/4000)

    def case_6(self):
        for _ in range(2):
            winsound.Beep(self.D, self.notetime//4)
            sleep(self.notetime/4000)

    def case_7(self):
        for _ in range(2):
            winsound.Beep(self.E, self.notetime//4)
            sleep(self.notetime/4000)

    def case_8(self):
        for _ in range(2):
            winsound.Beep(self.G, self.notetime//4)
            sleep(self.notetime/4000)

    def case_9(self):
        for _ in range(2):
            winsound.Beep(self.A, self.notetime//4)
            sleep(self.notetime/4000)


cases = Cases()

pg.init()

screen = pg.display.set_mode((200, 0))


def sair():
    pg.quit()
    sys.exit()


coord = 100, 500
keys = ''
while True:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sair()
        if event.type == pg.KEYDOWN:
            if event.unicode == '\r':
                if keys:
                    for dig in keys:
                        cases(dig)

                else:
                    while True:
                        keys = str(randrange(0, 9))
                        for dig in keys:
                            cases(dig)
                        user = input()
                        if user == keys:
                            print('ta certo')
                        else:
                            print(f'ta errado, era {keys}')
                        sleep(1)

            elif event.unicode == 'c':
                for dig in keys:
                    cases(dig)
            elif event.unicode == 'v':
                keys = ''
            else:
                keys += event.unicode

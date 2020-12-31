from PIL import Image
import pygame as pg
import numpy as np


class Parede:
    def __init__(self):
        map_img = Image.open('mapa.png')
        mapa_array_img = np.asarray(map_img)
        self.mapa = [[1 - rgb[0] // 255 for rgb in linha] for linha in mapa_array_img]
        self.Bsize = 20
        self.color = (130, 180, 240)

    def blit(self, window):
        for row, lista in enumerate(self.mapa):
            for col, value in enumerate(lista):
                if value:
                    pg.draw.rect(window, self.color, ((col*self.Bsize, row*self.Bsize), (self.Bsize, self.Bsize)))







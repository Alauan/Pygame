import pygame as pg
from math import sqrt, atan


def calc_wall_heights(mapa, pos, factor):
    distances = []
    for mapa_pos in mapa:
        distances.append(sqrt((pos[0]-mapa_pos[0])**2 + (pos[1]-mapa_pos[1])**2))

    wall_heights = []
    for distance in distances:
        wall_heights.append(1*factor/distance)

    return wall_heights


def calc_angles(mapa, pos):
    angles = []
    for mapa_pos in mapa:
        ca = (pos[0] - mapa_pos[0])
        co = (pos[1] - mapa_pos[1])
        if ca < 0:
            angles.append(180 + 57.295 * atan(co / ca))
        else:
            angles.append(57.295 * atan(co / ca))

    return angles


def render(mapa, pos):
    canvas = pg.Surface((700, 400))

    heights = calc_wall_heights(mapa, pos, 600)
    angles = calc_angles(mapa, pos)

    for index, angle in enumerate(angles):
        height = heights[index]
        ponto1 = (int((angle-40) * 7), 200 + height/2)
        ponto2 = (int((angle-40) * 7), 200 - height/2)
        pg.draw.line(canvas, (255, 255, 255), ponto1, ponto2)

    return canvas

from math import copysign, sqrt, pi, cos, sin, atan2
from typing import List, Union, Tuple
import pygame as pg
from PIL import Image
from random import random
import numpy as np
import sys


pg.init()
Clock = pg.time.Clock()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)


class Const:
    TILEWIDTH = 90
    TILEHEIGHT = 30
    SCREENWIDTH = screen.get_width()
    SCREENHEIGHT = screen.get_height()

    RIGHT = 1
    LEFT = 2
    TOP = 3
    BOTTOM = 4

    GREY = pg.Color((120, 125, 130))
    WHITE = pg.Color((255, 255, 255))
    BLUE = pg.Color((70, 70, 240))
    BLACK = pg.Color((20, 20, 20))
    RED = pg.Color((255, 50, 50))


def image_to_map(image_name):
    image = Image.open(image_name)
    data = list(image.getdata())
    width, height = image.size

    pixels = []
    for i in range(height):
        pixels.append([pixel[0] == 0 for pixel in data[i * width:i * width + width]])

    return pixels


class Plataforma:
    def __init__(self, width, surface, color, pos=0):
        self._surface = surface
        self.color = color
        self._width = width
        self._pos = pos

        self._surf_width = surface.get_width()
        self._surf_height = surface.get_height()
        self.rect = pg.Rect(self._pos, self._surf_height - 50, self._width, 20)
        self.velocity = 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new):
        self._width = new
        self.rect = pg.Rect(self._pos, self._surf_height - 50, self._width, 20)

    def move_to(self, x):
        ini_pos = self._pos
        if x < 0:
            self._pos = 0
        elif x > self._surf_width - self._width:
            self._pos = self._surf_width - self._width
        else:
            self._pos = x

        self.rect = pg.Rect(self._pos, self._surf_height - 50, self._width, 20)
        self.velocity = self._pos - ini_pos

    def draw(self):
        pg.draw.rect(self._surface, self.color, (self._pos, self._surf_height - 50, self._width, 20))


class Bola:
    def __init__(self, radius, surface, pos, color=(255, 255, 255), vel_y=3, vel_x=3):
        self._radius = radius
        self._pos = list(pos)
        self._vel_y = vel_y
        self._vel_x = vel_x
        self._vel = sqrt(vel_x ** 2 + vel_y ** 2)
        self.rotation = 0

        self.tail = []
        self.tail_points = []
        self.contador = 0
        self.overhang = 1.5

        self._surface = surface
        self._color = color

        self._surf_width = surface.get_width()
        self._surf_height = surface.get_height()

        self._collision_points_ref = [(cos(n * pi/4) * self._radius, sin(n * pi/4) * self._radius) for n in range(8)]
        self._collision_points = []

        # m -> pixel, s -> frame time
        self._spin = 0.1  # velocidade angular: rad/s
        self._mass = 1  # kg
        self._i = self._mass * self._radius ** 2  # momneto de inércia: kg m²
        self._ec_rot = (self._i * self._spin ** 2) / 2  # energia cinética: joules
        self._ec_x = (self._mass * self._vel_x ** 2) / 2  # energia de translação no eixo x: joules
        self._ec_y = (self._mass * self._vel_y ** 2) / 2  # energia de translação no eixo y: joules

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new):
        self._pos = new
        self._collision_points = [(x + new[0], y + new[1]) for x, y in self._collision_points_ref]

    @property
    def vel_x(self):
        return self._vel_x

    @vel_x.setter
    def vel_x(self, new):
        self._vel_x = new
        self._ec_x = (self._mass * self._vel_x ** 2) / 2
        self._vel = sqrt(self.vel_x ** 2 + self.vel_y ** 2)

    @property
    def vel_y(self):
        return self._vel_y

    @vel_y.setter
    def vel_y(self, new):
        self._vel_y = new
        self._ec_y = (self._mass * self._vel_y ** 2) / 2
        self._vel = sqrt(self.vel_x ** 2 + self.vel_y ** 2)

    @property
    def spin(self):
        return self._spin

    @spin.setter
    def spin(self, new):
        self._spin = new
        self._i = self._mass * self._radius ** 2
        self._ec_rot = (self._i * self._spin ** 2) / 2

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, new):
        self._mass = new
        self._i = self._mass * self._radius ** 2
        self._ec_rot = (self._i * self._spin ** 2) / 2

    def move(self, gravity=0.0):
        self.rotation += self.spin
        self.pos = [self.pos[0] + self.vel_x, self.pos[1] + self.vel_y]
        self.vel_y += gravity

    def aero_move(self, gravity=0.0, drag=0.004):
        k = 0.01
        self.vel_x += self.spin * self.vel_y * k
        self.vel_y -= self.spin * self.vel_x * k

        self.vel_x -= self.vel_x * drag
        self.vel_y -= self.vel_y * drag
        self.spin -= self.spin * drag

        self.move(gravity)

    def collidemap(self, tile_map, tile_width, tile_height) -> Tuple[int, int, int]:
        """ Return the side on witch the ball collided with any tile in a map and the tile indexes"""
        row1 = int((self.pos[1] - self._radius) // tile_height)
        row2 = int((self.pos[1] + self._radius)//tile_height + 1)
        col1 = int((self.pos[0] - self._radius)//tile_width)
        col2 = int((self.pos[0] + self._radius)//tile_width + 1)
        in_range = np.array(tile_map, dtype=object)[row1:row2, col1:col2]

        for y, row in enumerate(in_range):
            for x, rect in enumerate(row):
                if rect:
                    side = self.colliderect(rect)
                    if side:
                        return side, y + row1, x + col1
        return 0, 0, 0

    def colliderect(self, rect):
        """ return the side in witch the ball hit a rectangle"""
        for point in self._collision_points:
            if rect.collidepoint(point[0] + self.vel_x, point[1]):
                if self.vel_x > 0:
                    return Const.LEFT
                if self.vel_x < 0:
                    return Const.RIGHT
            if rect.collidepoint(point[0], point[1] + self.vel_y):
                if self.vel_y > 0:
                    return Const.BOTTOM
                if self.vel_y < 0:
                    return Const.TOP

    def collidesurf(self):
        """ returns the side on witch the ball hit its own surface border"""
        x = self.pos[0] + self._vel_x + copysign(self._radius, self._vel_x)
        y = self.pos[1] + self._vel_y + copysign(self._radius, self._vel_y)

        if x < 0:
            return Const.LEFT
        if x > self._surf_width:
            return Const.RIGHT
        if y < 0:
            return Const.TOP
        if y > self._surf_height:
            return Const.BOTTOM

    def random_hit(self, side):
        """ a hit that the absolute _velocity is kept but the X and Y velocities are changed randomly"""
        k = random()

        self._vel_x = sqrt(self._vel ** 2 * k) * copysign(1, self._vel_x)
        self._vel_y = sqrt(self._vel ** 2 * (1 - k)) * copysign(1, self._vel_y)
        if side in (Const.RIGHT, Const.LEFT):
            self._vel_x *= -1
        else:
            self._vel_y *= -1

    def spin_hit(self, side, spin_grip=0.2, move_grip=0.2, plat_vel=0.0, bump=0.0):
        """ a hit with spin """
        if side:
            self.update_tail()

        if not 0 <= spin_grip <= 1 or not 0 <= move_grip <= 1:
            raise ValueError("grip must be between 0 and 1")

        ini_ec_y = self._ec_y
        ini_ec_x = self._ec_x
        if side == Const.RIGHT:
            self.vel_y = copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) * move_grip + self.vel_y * (1 - move_grip)
            self.vel_x = self.vel_x * -1 - copysign(bump, self.vel_x)
            self.spin = copysign(sqrt(ini_ec_y * 2 / self._i) * spin_grip, self.vel_y) + self.spin * (1 - spin_grip)
        elif side == Const.LEFT:
            self.vel_y = -copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) * move_grip + self.vel_y * (1 - move_grip)
            self.vel_x = self.vel_x * -1 - copysign(bump, self.vel_x)
            self.spin = -copysign(sqrt(ini_ec_y * 2 / self._i) * spin_grip, self.vel_y) + self.spin * (1 - spin_grip)
        elif side == Const.TOP:
            self.vel_x = copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) * move_grip + self.vel_x * (1 - move_grip)
            self.vel_y = self.vel_y * -1 - copysign(bump, self.vel_y)
            self.spin = copysign(sqrt(ini_ec_x * 2 / self._i) * spin_grip, self.vel_x) + self.spin * (1 - spin_grip)
        elif side == Const.BOTTOM:
            vel_rel = self.vel_x - plat_vel
            self.vel_x = -(copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) - plat_vel) * move_grip + self.vel_x * (1 - move_grip)
            self.vel_y = self.vel_y * -1 - copysign(bump, self.vel_y)
            self.spin = -copysign(sqrt(self.mass * vel_rel ** 2 * 2 / self._i) * spin_grip, vel_rel) + self.spin * (1 - spin_grip)

    def normal_hit(self, side):
        """ a hit that just changes the sign of Y or X _velocity """
        if side in (Const.RIGHT, Const.LEFT):
            self.vel_x *= -1
        else:
            self.vel_y *= -1

    def update_tail(self):
        self.overhang = 2
        self.tail.append((atan2(self.vel_y, self.vel_x), self.pos))
        self.tail_points = []
        for index, info in enumerate(self.tail):
            angle, pos = info
            self.tail_points.append((cos(angle + pi / 2) * (self._radius * (index * self.overhang / len(self.tail))) + pos[0],
                                     sin(angle + pi / 2) * (self._radius * (index * self.overhang / len(self.tail))) + pos[1]))

        for index, info in sorted(enumerate(self.tail), reverse=True):
            angle, pos = info
            self.tail_points.append((cos(angle - pi / 2) * (self._radius * (index * self.overhang / len(self.tail))) + pos[0],
                                     sin(angle - pi / 2) * (self._radius * (index * self.overhang / len(self.tail))) + pos[1]))

        if len(self.tail) > 10:
            self.tail.pop(0)

    def draw(self):
        # tail
        r = abs(self.spin) * 40
        r = 255 if r > 255 else r
        b = abs(255 - abs(self.spin) * 40)
        b = 255 if b > 255 else b
        tail_color = (r, 30, b)

        self.contador += 1
        if not self.contador % 3:
            self.contador = 0
            self.update_tail()

        if len(self.tail) > 3:
            angle, pos = atan2(self.vel_y, self.vel_x), self.pos
            self.tail_points[len(self.tail)-1] = (cos(angle + pi / 2) * self._radius * self.overhang + pos[0],
                                                  sin(angle + pi / 2) * self._radius * self.overhang + pos[1])
            self.tail_points[len(self.tail)] = (cos(angle - pi / 2) * self._radius * self.overhang + pos[0],
                                                sin(angle - pi / 2) * self._radius * self.overhang + pos[1])

            pg.draw.polygon(self._surface, tail_color, self.tail_points)

        pg.draw.circle(self._surface, tail_color, self.pos, self._radius * self.overhang)

        # ball
        pg.draw.circle(self._surface, self._color, self.pos, self._radius)
        pg.draw.arc(self._surface, Const.BLACK, (self.pos[0] - self._radius, self.pos[1] - self._radius,
                                               self._radius * 2, self._radius * 2), self.rotation,
                    self.rotation + pi / 2, self._radius)


class Main:
    @staticmethod
    def level():
        plat = Plataforma(600, screen, Const.WHITE)
        balls = [Bola(10, screen, (800, 600))]
        mouse_pos = (0, 0)
        mouse_bt = 0
        plat_modes = {0: {'color': Const.WHITE, 'spin': 0.4, 'move': 0.4},
                      1: {'color': Const.BLUE, 'spin': 0.6, 'move': 0.2},
                      3: {'color': Const.BLACK, 'spin': 0.2, 'move': 0.6}}
        pg.mouse.set_visible(False)

        mapa = image_to_map('map.png')
        tiles = []
        for y, lista in enumerate(mapa):
            tiles.append([])
            for x, value in enumerate(lista):
                if value:
                    tiles[y].append(pg.Rect(x * Const.TILEWIDTH + 1, y * Const.TILEHEIGHT + 1,
                                            Const.TILEWIDTH - 1, Const.TILEHEIGHT - 1))
                else:
                    tiles[y].append(None)

        while True:
            screen.fill(Const.GREY)
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    mouse_pos = event.pos
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button != 2:
                        mouse_bt = event.button
                if event.type == pg.MOUSEBUTTONUP:
                    mouse_bt = 0

            for index, ball in sorted(enumerate(balls), reverse=True):
                # platform collide
                side = ball.colliderect(plat.rect)
                if side:
                    ball.spin_hit(side, plat_modes[mouse_bt]['spin'], plat_modes[mouse_bt]['move'], plat.velocity, 1.2)
                # surface border collide
                side = ball.collidesurf()
                if side == Const.BOTTOM:
                    balls.append(Bola(10, screen, (800, 600)))
                    balls.pop(index)
                elif side:
                    ball.spin_hit(side, 0.1, 0.1, bump=1)
                # tile collide
                side, y, x = ball.collidemap(tiles, Const.TILEWIDTH, Const.TILEHEIGHT)
                if side:
                    if abs(ball.spin) > 0.3:
                        ball.spin -= copysign(0.2, ball.spin)
                    else:
                        ball.spin_hit(side)
                    tiles[y][x] = None

            plat.color = plat_modes[mouse_bt]['color']
            plat.move_to(mouse_pos[0] - plat.width / 2)
            plat.draw()

            for ball in balls:
                ball.aero_move(0.07)
                ball.draw()

            for row in tiles:
                for tile in row:
                    if tile:
                        screen.fill(Const.WHITE, tile)

            pg.display.update()
            Clock.tick(60)


if __name__ == '__main__':
    Main.level()

from math import copysign, sqrt, pi
import pygame as pg
from PIL import Image
from random import random
import sys

pg.init()
Clock = pg.time.Clock()
screen = pg.display.set_mode((900, 500))

TILEWIDTH = 45
TILEHEIGHT = 15


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
        self._color = color
        self._width = width
        self._pos = pos

        self._surf_width = surface.get_width()
        self._surf_height = surface.get_height()
        self.rect = pg.Rect(self._pos, self._surf_height - 50, self._width, 20)
        self._velocity = [0, 0, 0]

    @property
    def velocity(self):
        return sum(self._velocity)/len(self._velocity)

    @velocity.setter
    def velocity(self, new):
        self._velocity.append(new)
        self._velocity.pop(0)

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
        pg.draw.rect(self._surface, self._color, (self._pos, self._surf_height - 50, self._width, 20))


class Bola:
    def __init__(self, radius, surface, pos, color=(255, 255, 255), vel_y=3, vel_x=3):
        self._radius = radius
        self.pos = list(pos)
        self._vel_y = vel_y
        self._vel_x = vel_x
        self._vel = sqrt(vel_x ** 2 + vel_y ** 2)
        self.rotation = 0

        self._surface = surface
        self._color = color

        self._surf_width = surface.get_width()
        self._surf_height = surface.get_height()

        # m -> pixel, s -> frame time
        self._spin = 0.1  # velocidade angular: rad/s
        self._mass = 1  # kg
        self._i = self._mass * self._radius ** 2  # momneto de inércia: kg m²
        self._ec_rot = (self._i * self._spin ** 2) / 2  # energia cinética: joules
        self._ec_x = (self._mass * self._vel_x ** 2) / 2  # energia de translação no eixo x: joules
        self._ec_y = (self._mass * self._vel_y ** 2) / 2  # energia de translação no eixo y: joules

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
        self.pos[0] += self._vel_x
        self.pos[1] += self._vel_y
        self.vel_y += gravity

    def aero_move(self, gravity=0.0, drag=0.005):
        k = 0.02
        self.vel_x += self.spin * self.vel_y * k
        self.vel_y -= self.spin * self.vel_x * k

        self.vel_x -= self.vel_x * drag
        self.vel_y -= self.vel_y * drag
        self.spin -= self.spin * drag

        self.move(gravity)

    def colliderect(self, rect):
        """ return the side in witch the ball hit a rectangle"""
        x = self.pos[0] + self.vel_x + copysign(self._radius, self._vel_x)
        y = self.pos[1] + self.vel_y + copysign(self._radius, self._vel_y)

        if rect.collidepoint(x, self.pos[1]):
            if self.vel_x > 0:
                return 'left'
            if self.vel_x < 0:
                return 'right'
        if rect.collidepoint(self.pos[0], y):
            if self.vel_y > 0:
                return 'bottom'
            if self.vel_y < 0:
                return 'top'

    def collidesurf(self):
        """ returns the side on witch the ball hit its own surface border"""
        x = self.pos[0] + self._vel_x + copysign(self._radius, self._vel_x)
        y = self.pos[1] + self._vel_y + copysign(self._radius, self._vel_y)

        if x < 0:
            return 'left'
        if x > self._surf_width:
            return 'right'
        if y < 0:
            return 'top'
        if y > self._surf_height:
            return 'bottom'

    def random_hit(self, is_horizontal: bool):
        """ a hit that the absolute _velocity is kept but the X and Y velocities are changed randomly"""
        k = random()

        self._vel_x = sqrt(self._vel ** 2 * k) * copysign(1, self._vel_x)
        self._vel_y = sqrt(self._vel ** 2 * (1 - k)) * copysign(1, self._vel_y)
        if is_horizontal:
            self._vel_x *= -1
        else:
            self._vel_y *= -1

    def spin_hit(self, side, grip=0.2, plat_vel=0.0, bump=1.0):
        """ a hit with spin """
        if not 0 <= grip <= 1:
            raise ValueError("grip must be between 0 and 1")

        ini_ec_y = self._ec_y
        ini_ec_x = self._ec_x
        if side == 'right':
            self.vel_y = copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) * grip + self.vel_y * (1 - grip)
            self.vel_x *= -1
            self.spin = copysign(sqrt(ini_ec_y * 2 / self._i) * grip, self.vel_y) + self.spin * (1 - grip)
        elif side == 'left':
            self.vel_y = -copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) * grip + self.vel_y * (1 - grip)
            self.vel_x *= -1
            self.spin = -copysign(sqrt(ini_ec_y * 2 / self._i) * grip, self.vel_y) + self.spin * (1 - grip)
        elif side == 'top':
            self.vel_x = copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) * grip + self.vel_x * (1 - grip)
            self.vel_y *= -1
            self.spin = copysign(sqrt(ini_ec_x * 2 / self._i) * grip, self.vel_x) + self.spin * (1 - grip)
        elif side == 'bottom':
            vel_rel = self.vel_x - plat_vel
            self.vel_x = -(copysign(sqrt(self._ec_rot * 2 / self.mass), self.spin) - plat_vel) * grip \
                         + self.vel_x * (1 - grip)
            self.vel_y *= -1 * bump
            self.spin = -copysign(sqrt(self.mass * vel_rel ** 2 * 2 / self._i) * grip, vel_rel) + self.spin * (1 - grip)

    def normal_hit(self, side):
        """ a hit that just changes the sign of Y or X _velocity """
        if side in ('right', 'left'):
            self.vel_x *= -1
        else:
            self.vel_y *= -1

    def draw(self):
        pg.draw.circle(self._surface, self._color, self.pos, self._radius)
        pg.draw.arc(self._surface, (255, 50, 50), (self.pos[0] - self._radius, self.pos[1] - self._radius,
                                                   self._radius * 2, self._radius * 2), self.rotation,
                    self.rotation + pi / 2, 6)


plat = Plataforma(300, screen, (255, 255, 255))
balls = [Bola(10, screen, (400, 200), vel_x=0)]

mapa = image_to_map('map.png')
tiles = []
for y, lista in enumerate(mapa):
    for x, value in enumerate(lista):
        if value:
            tiles.append(pg.Rect(x * TILEWIDTH + 1, y * TILEHEIGHT + 1, TILEWIDTH - 1, TILEHEIGHT - 1))

while True:
    mouse_pos = []
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEMOTION:
            mouse_pos = event.pos

    balls_to_pop = []
    tiles_to_pop = []
    for index, ball in enumerate(balls):
        # platform collide
        if ball.colliderect(plat.rect):
            ball.spin_hit('bottom', 0.3, plat.velocity, 1.05)
        # surface border collide
        elif ball.collidesurf() == 'bottom':
            balls_to_pop.append(index)
        elif ball.collidesurf():
            ball.spin_hit(ball.collidesurf(), 0.1)
        # tile collide
        for b, tile in enumerate(tiles):
            if ball.colliderect(tile):
                if abs(ball.spin) > 0.3:
                    ball.spin -= copysign(0.2, ball.spin)
                else:
                    ball.spin_hit(ball.colliderect(tile))
                tiles_to_pop.append(b)

    for ball in balls_to_pop:
        balls.pop(ball)
        balls.append(Bola(10, screen, (400, 200), vel_x=0))
    for tile in tiles_to_pop[::-1]:
        tiles.pop(tile)

    if mouse_pos:
        plat.move_to(mouse_pos[0] - plat.width / 2)
    plat.draw()

    for ball in balls:
        ball.aero_move(0.07)
        ball.draw()

    for tile in tiles:
        screen.fill((50, 50, 250), tile)

    pg.display.update()
    Clock.tick(60)

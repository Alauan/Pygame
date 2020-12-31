import numpy as np
from random import getrandbits


class Sand:
    def __init__(self, grid_dimensions, pygame_window, color):
        self.grid_dimensions = grid_dimensions
        self.grid_moving = np.zeros(grid_dimensions, dtype='bool')
        self.grid_static = np.zeros(grid_dimensions, dtype='bool')
        self.window = pygame_window
        self.color = color

    def pour(self, grid_position):
        x = grid_position[0]
        y = grid_position[1]
        self.grid_moving[y, x] = True

    def move(self):
        for row, lista in enumerate(self.grid_moving[::-1]):
            row = self.grid_dimensions[0] - row - 1
            if getrandbits(1):
                for col, value in enumerate(lista):
                    if value:
                        moveu = False
                        if row + 1 < self.grid_dimensions[1]:

                            # Vê se tem pra onde ir
                            if not self.grid_static[row + 1, col] and not self.grid_moving[row + 1, col]:
                                self.grid_moving[row + 1, col] = True
                                self.grid_moving[row, col] = False
                                moveu = True

                            elif getrandbits(1):
                                if col + 1 < self.grid_dimensions[0] and not self.grid_static[row + 1, col + 1] \
                                        and not self.grid_moving[row + 1, col + 1]:
                                    self.grid_moving[row + 1, col + 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True

                                elif col - 1 > 0 and not self.grid_static[row + 1, col - 1] \
                                        and not self.grid_moving[row + 1, col - 1]:
                                    self.grid_moving[row + 1, col - 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True
                            else:
                                if col - 1 > 0 and not self.grid_static[row + 1, col - 1] \
                                        and not self.grid_moving[row + 1, col - 1]:
                                    self.grid_moving[row + 1, col - 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True

                                elif col + 1 < self.grid_dimensions[0] and not self.grid_static[row + 1, col + 1] \
                                        and not self.grid_moving[row + 1, col + 1]:
                                    self.grid_moving[row + 1, col + 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True

                        if not moveu:
                            self.grid_static[row, col] = True
                            self.grid_moving[row, col] = False
            else:
                for col, value in enumerate(lista[::-1]):
                    col = self.grid_dimensions[1] - col - 1
                    if value:
                        moveu = False
                        if row + 1 < self.grid_dimensions[1]:

                            # Vê se tem pra onde ir
                            if not self.grid_static[row + 1, col] and not self.grid_moving[row + 1, col]:
                                self.grid_moving[row + 1, col] = True
                                self.grid_moving[row, col] = False
                                moveu = True

                            elif getrandbits(1):
                                if col + 1 < self.grid_dimensions[0] and not self.grid_static[row + 1, col + 1] \
                                        and not self.grid_moving[row + 1, col + 1]:
                                    self.grid_moving[row + 1, col + 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True

                                elif col - 1 > 0 and not self.grid_static[row + 1, col - 1] \
                                        and not self.grid_moving[row + 1, col - 1]:
                                    self.grid_moving[row + 1, col - 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True
                            else:
                                if col - 1 > 0 and not self.grid_static[row + 1, col - 1] \
                                        and not self.grid_moving[row + 1, col - 1]:
                                    self.grid_moving[row + 1, col - 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True

                                elif col + 1 < self.grid_dimensions[0] and not self.grid_static[row + 1, col + 1] \
                                        and not self.grid_moving[row + 1, col + 1]:
                                    self.grid_moving[row + 1, col + 1] = True
                                    self.grid_moving[row, col] = False
                                    moveu = True

                        if not moveu:
                            self.grid_static[row, col] = True
                            self.grid_moving[row, col] = False

    def blit(self):
        for row, lista in enumerate(self.grid_static):
            for col, value in enumerate(lista):
                if value:
                    self.window.fill(self.color, ((col*2, row*2), (2, 2)))
                if self.grid_moving[row, col]:
                    self.window.fill((250, 150, 150), ((col * 2, row * 2), (2, 2)))



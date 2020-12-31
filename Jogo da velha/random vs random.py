import numpy as np
from random import choice

# Tabuleiro
tabuleiro = np.zeros((3, 3), dtype='int')


def result(space):
    for row in space:
        if all(b == 1 for b in row):
            return 'lost'
        if all(b == 2 for b in row):
            return 'won'
    for col in np.rot90(space):
        if all(b == 1 for b in col):
            return 'lost'
        if all(b == 2 for b in col):
            return 'win'

    if space[0][0] == space[1][1] == space[2][2] == 1 or \
        space[0][2] == space[1][1] == space[2][0] == 1:
        return 'lost'

    if space[0][0] == space[1][1] == space[2][2] == 2 or \
        space[0][2] == space[1][1] == space[2][0] == 2:
        return 'win'

    if all(all(b > 0 for b in row) for row in space):
        return 'draw'


jogadas = 0
Ai = {'input': list(), 'output': list()}
fails = list()
wins = list()
Nwins = 0
for i in range(10000):

    possible = list()
    for a in range(3):
        for c in range(3):
            possible.append((a, c))

    while result(tabuleiro) is None:

        coord = choice(possible)
        # colocando as jogadas na Ai
        if jogadas % 2:
            Ai['output'].append(coord)
        else:
            Ai['input'].append(coord)

        possible.remove(coord)
        tabuleiro[coord[0], coord[1]] = 2 if jogadas % 2 else 1
        jogadas += 1

    # contabilizando as vitórias
    if result(tabuleiro) == 'win':
        Nwins += 1

    # Limpando a AI e o tabuleiro
    Ai['input'] = list()
    Ai['output'] = list()
    tabuleiro = np.zeros((3, 3), dtype='int')

print(Nwins / 100)

import numpy as np
import pickle
ClassAI = __import__('ClassAI')


def result(space):
    for row in space:
        if all(b == 1 for b in row):
            return 'roberto'
        if all(b == 2 for b in row):
            return 'jonas'
    for col in np.rot90(space):
        if all(b == 1 for b in col):
            return 'roberto'
        if all(b == 2 for b in col):
            return 'jonas'

    if space[0][0] == space[1][1] == space[2][2] == 1 or \
       space[0][2] == space[1][1] == space[2][0] == 1:
        return 'roberto'

    if space[0][0] == space[1][1] == space[2][2] == 2 or \
       space[0][2] == space[1][1] == space[2][0] == 2:
        return 'jonas'

    if all(all(b > 0 for b in row) for row in space):
        return 'draw'


possible = list()
roberto = ClassAI.AI(dict())  # jogador (1)
jonas = ClassAI.AI(dict())    # jogador (2)
resultado = ''

ciclos = int(input('Com quantos ciclos treinar a IA?  '))
for cont in range(1, ciclos+1):
    # --------------------------------------- Pré partida ------------------------------------------
    # Limpando o tabuleiro, e as possibilidades

    tabuleiro = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]

    possible.clear()
    for a in range(3):
        for c in range(3):
            possible.append((a, c))
    # ------------------------------------------ Partida --------------------------------------------
    quickBreak = False
    while not quickBreak:

        """-------------- jogada do Roberto (1) ------------------"""
        resultado = result(tabuleiro)
        if resultado == 'jonas':        # se o jonas venceu
            roberto.armazenar()             # armazena a falha no roberto
            jonas.armazenar(False)
            break                           # para a partida
        elif resultado == 'draw':
            break
        else:

            escolha = roberto.escolher(tabuleiro, possible)
            roberto.tab(tabuleiro)

            tabuleiro[escolha[0]][escolha[1]] = 1   # coloca a escolha no tabuleiro
            possible.remove(escolha)                # remove a escolha de possible

        """--------------- jogada do Jonas (2) --------------------"""
        resultado = result(tabuleiro)
        if resultado == 'roberto':        # se o roberto venceu
            jonas.armazenar()             # armazena a falha no jonas
            roberto.armazenar(False)
            break                           # para a partida
        elif resultado == 'draw':
            break
        else:
            escolha = jonas.escolher(tabuleiro, possible)
            jonas.tab(tabuleiro)

            tabuleiro[escolha[0]][escolha[1]] = 2   # coloca a escolha no tabuleiro
            possible.remove(escolha)                # remove a escolha de possible

    # --------------------------------------- pós partida --------------------------------------------------
    # contabilizando as vitórias
    if cont >= ciclos - 4000:
        if resultado == 'roberto':
            roberto.Nwins += 1

        if resultado == 'jonas':
            jonas.Nwins += 1

    roberto.historico.clear()
    jonas.historico.clear()

    # printando a porcentagem dos ciclos
    if cont * 100 % ciclos == 0:
        print(f'{cont * 100 / ciclos}%')

print(f'Treinamento concluído!')

memoryOut = open('memoryFirst.pickle', 'wb')
pickle.dump(roberto.memoria, memoryOut)
memoryOut.close()

memoryOut = open('memorySecond.pickle', 'wb')
pickle.dump(jonas.memoria, memoryOut)
memoryOut.close()

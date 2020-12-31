import numpy as np
largura = 2
altura = 2

quadrada = altura == largura
dgl_principal = list()
dgl_secundaria = list()
matriz = np.zeros((altura, largura), dtype='int')


for row in range(altura):
    x = row + 1
    for col in range(largura):
        y = col + 1

        elemento = (x-y)**2
        matriz[row, col] = elemento

        if quadrada and row == col:
            dgl_principal.append(elemento)
        if quadrada and row + col == largura-1:
            dgl_secundaria.append(elemento)


for i in matriz:
    print(i)
if quadrada:
    print(f'A diagonal principal é: {dgl_principal}')
    print(f'A diagonal secundaria é: {dgl_secundaria}')

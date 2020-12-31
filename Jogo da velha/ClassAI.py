from random import choice


class AI:
    def __init__(self, memoria):
        self.memoria = memoria                # {mapa: possibilidades}
        self.historico = list()             # historico da partida [(mapa, coord), (...), ...]
        self.coord = ''                     # coordenada escolhida por último
        self.Nwins = 0                      # contador de número de vitórias

    def tab(self, mapa):
        """transforma o tabuleiro e seus itens em tuplas e armazena em historico"""
        mapa = mapa[:]  # mapa é igual a sua cópia para evitar interações com o resto do programa
        for index, i in enumerate(mapa):  # transforma mapa em uma tupla
            mapa[index] = tuple(i)
        self.historico.append((tuple(mapa), self.coord))

    def escolher(self, mapa, possibilidades):
        """ sistema de escolha levando em consideração as falhas semelhantes """
        mapa = mapa[:]                      # mapa é igual a sua cópia para evitar interações com o resto do programa
        for index, i in enumerate(mapa):    # transforma mapa em uma tupla
            mapa[index] = tuple(i)
        mapa = tuple(mapa)

        if mapa in self.memoria:          # se existir falha semelhante
            if len(self.memoria[mapa]) >= 1:
                self.coord = choice(self.memoria[mapa])
                return self.coord

        self.coord = choice(possibilidades)
        return self.coord

    def armazenar(self, derrota=True):
        """ sistema de armazenamento """
        # analisa cada jogada, da última à primeira
        for jogada in reversed(self.historico):
            mapa = jogada[0]
            coord = jogada[1]
            if mapa in self.memoria:                # se o mapa já estiver em memoria
                if len(self.memoria[mapa]) >= 1:      # se o mapa ainda tiver possibilidades
                    if derrota:                           # se for derrota
                        while coord in self.memoria[mapa]:
                            self.memoria[mapa].remove(coord)  # remove a coordenada e para o armazenamento
                        break
                    else:                               # se for vitória
                        self.memoria[mapa].append(coord)
                        break

            else:                                 # se ainda não está em memoria
                # calcular as possibilidades de jogada do mapa
                possibilidades = list()
                for row, l in enumerate(mapa):
                    for col, value in enumerate(l):
                        if value == 0:
                            possibilidades.append((row, col))

                self.memoria[mapa] = possibilidades  # colocar mapa em memoria
                if derrota:
                    self.memoria[mapa].remove(coord)  # remove a coordenada e para o armazenamento

                break

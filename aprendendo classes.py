class Carro:
    def __init__(self, marca, potencia, combustivel):
        self.marca = marca
        self.potencia = potencia
        self.combustivel = combustivel

    @staticmethod
    def ligar():
        print('O carro está ligando...')

    @staticmethod
    def desligar():
        print('Carro desligando...')

    def especificacoes(self):
        print(self.marca, self.potencia, self.combustivel)


class Fusca(Carro):
    def __init__(self, marca, potencia, combustivel, porta_malas, dois_cilindros):
        super().__init__(marca, potencia, combustivel)
        self.porta_malas = porta_malas
        self.dois_cilindros = dois_cilindros

    @staticmethod
    def fazer_drift():
        super().ligar()
        print('skrrrrrrr')

    def onde_ta_a_mala(self):
        print(f'A mala está {self.porta_malas}')

    def e_dois_cilindros(self):
        print(self.dois_cilindros)

    def potencia(self):
        print(self.potencia)


Herby = Fusca('wolksvawen', '400hp', 'gasolina', 'na frente', True)
Herby.ligar()
Herby.especificacoes()
Herby.fazer_drift()
Herby.desligar()
Herby.onde_ta_a_mala()
Herby.e_dois_cilindros()
Herby.potencia()

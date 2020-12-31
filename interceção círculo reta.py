from math import sqrt

try:
    # definindo o círculo:
    yo = 3  # coordenada do centro
    xo = 2
    r = 4  # raio

    # definindo a reta:
    x = -3

    # calculando o ponto de interseção
    b = -2 * yo
    c = yo**2 - (r**2 - (x - xo)**2)
    y = (-b + sqrt(b**2 - 4*c)) / 2  # bascara
    print(y)

except:
    print('a reta não tem pontos em comum com o círculo')

class Level:
    def __call__(self, index):
        return getattr(self, 'lv_' + str(index), lambda: print('Esse nível não existe'))

    def lv_1:


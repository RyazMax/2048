# Игра 2048
# Рязанов Максим

from random import randint


class Game:
    # Инициализая поля
    def __init__(self, width, max_value, chance=0.9):
        self.mat = [[0]*width for i in range(width)]
        self.width = width
        self.count = 0
        self.max_value = max_value
        self.chance = chance
        self.avail_turns = 'wasd'

    def get_avail(self):
        res = []
        for i in range(self.width):
            for j in range(self.width):
                if self.mat[i][j] == 0:
                    res.append((i,j))
        return res

    def copy_mat(self, mat, mode=0):
        res = [[0]*self.width for i in range(self.width)]
        for i in range(self.width):
            for j in range(self.width):
                if mode:
                    res[j][i] = (mat[i][j])
                else:
                    res[i][j] = mat[i][j]
        return res

    def new_cell(self):
        avail = self.get_avail()
        if len(avail) > 0:
            new = avail[randint(0,len(avail)-1)]
            k = randint(0,100)
            if k> self.chance*100:
                self.mat[new[0]][new[1]] = 4
            else:
                self.mat[new[0]][new[1]] = 2
            return list(new)

    def turn(self, direct='a'):
        # Сдвиг
        g = False
        com_last = 0
        delta = 1
        end = self.width
        new = []
        if direct in 'ds':
            com_last = self.width-1
            delta = -1
            end = -1
        if direct in 'ws':
            mat = self.copy_mat(self.mat, 1)
        else:
            mat = self.copy_mat(self.mat, 0)

        for i in range(self.width):
            last = com_last
            for j in range(com_last+delta, end, delta):
                if mat[i][j]:
                    if mat[i][last] == mat[i][j]:
                            mat[i][last] *= 2
                            mat[i][j] = 0
                            g = True
                            if direct in 'ad':
                                new.append((i,last))
                            else: new.append((last,i))
                            last += delta
                    else:
                        if mat[i][last]:
                            if last+delta != j: g = True
                            t, mat[i][j] = mat[i][j], 0
                            mat[i][last+delta] = t
                            last += delta
                        else:
                            mat[i][last], mat[i][j] = mat[i][j], 0
                            g = True
        if direct in 'ws': mat = self.copy_mat(mat,1)
        return mat, g, new

    def check(self):
        self.avail_turns = ''
        for i in 'wasd':
            if self.turn(i)[1]: self.avail_turns += i

    def make_turn(self,direct):
        if direct in self.avail_turns:
            self.mat, g, new = self.turn(direct)
            k = self.new_cell()
            self.check()
            return True, new+[k]
        else:
            return False, []

    def show_board(self):
        for i in range(self.width):
            for j in range(self.width):
                print(self.mat[i][j],end = '\t')
            print()


if __name__ == '__main__':
    width = input('Введите размер')
    if width: width = int(width)
    else: width = 4
    chance = input('Введите шанс 4')
    if chance: chance = float(chance)
    else: chance = 0.9

    game = Game(width,0,chance)

    g = False
    while game.avail_turns:
        game.show_board()
        turn = input()
        game.make_turn(turn)
    game.show_board()
    print('Вы проиграли')

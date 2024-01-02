from random import randint as rnd

class Ship:
    def __init__(self, x, y, length, rot):
        self.x = x
        self.y = y
        self.length = length
        self.rot = rot
        self.life = length


class Board:
    def __init__(self, width = 6, height = 6,):
        self.width = width
        self.height = height
        self.board = []
        yach = []
        for i in range(self.height):
            for j in range(self.width):
                yach.append(None)
            self.board.append(yach)
            yach = []
    def print(self, hide = False):
        numst = 1
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in self.board:
            st = str(numst) +' | '
            for j in i:
                if j == None or (type(j) == Ship and hide):
                    st = st + 'O' + ' | '
                elif j == 0:
                    st = st + str(j) + ' | '
                elif type(j) == Ship and not hide:
                    st = st + '■' + ' | '
                elif j == 2:
                    st = st + 'X' + ' | '
                elif j == 3:
                    st = st + 'T' + ' | '
            print(st)
            numst += 1

class GenerateShipSet:
    def __init__(self, board):
        self.ship_set = []
        self.board = board

    def start_gen(self):
        #1 трехпалубный, 3 двухпалубных, 4 однопалубных
        countlist = [(1, 3), (2, 2), (4, 1)]
        for i in countlist:
            for j in range(i[0]):
                try:
                    self.generate(i[1])
                except RecursionError:
                    # print('recurs')
                    for i in range(6):
                        for j in range(6):
                            self.board[i][j] = None
                    self.ship_set = []
                    return self.start_gen()

    def generate(self, length):
        l = length
        chek_list = [(0,0),(-1,0),(0,-1),(1,0),(0,1)]
        coord = GenerateShipSet.dotrandom(l)
        o = coord[0]
        x = coord[1]
        y = coord[2]
        # print(x + 1, y + 1)
        if o == 0:
            for i in range(l):
                for j in chek_list:
                    if x + j[0] + i < 6 and y+j[1] < 6 and x + j[0] + i >= 0 and y+j[1] >= 0:
                        if self.board[y+j[1]][x + j[0] + i] != None:
                                return self.generate(l)

            s = Ship(x, y, l, o)
            self.ship_set.append(s)
            # print('compl')
            for i in range(l):
                self.board[y][x + i] = self.ship_set[-1]

        elif o == 1:
            for i in range(l):
                for j in chek_list:
                    if x + j[0] < 6 and y + j[1] + i < 6 and x + j[0] >= 0 and y + j[1] + i >= 0:
                        if self.board[y+j[1] + i][x + j[0]] != None:
                                # print('busy')
                                return self.generate(l)
            s = Ship(x, y, l, o)
            self.ship_set.append(s)
            # print('compl')
            for i in range(l):
                self.board[y + i][x] = self.ship_set[-1]
    @staticmethod
    def dotrandom(l):
        lr = l
        o = rnd(0, 1)
        x = rnd(0, 5)
        y = rnd(0, 5)
        if x + lr > 5 or y + lr > 5:
            return GenerateShipSet.dotrandom(lr)
        return o, x, y
class Shoot():
    def __init__(self, board):
        self.board = board
        self.count = 0

    def player(self):
        try:
            x = int(input('Введите координату X: '))
            y = int(input('Введите координату Y: '))
        except ValueError:
            print('Попробуйте ещё раз:/')
            return self.player()
        self.check_shot(x, y)
        return

    def check_shot(self, x, y):
        if x > 6 or y > 6 or x < 1 or y < 1:
            print('Вы стреляете мимо доски.')
            return self.player()
        x -= 1
        y -= 1
        if self.board[y][x] == None:
            self.board[y][x] = 3
            print('-' * 20)
            print('Мимо!')
            print('-' * 20)
            return
        if type(self.board[y][x]) == Ship:
            self.board[y][x].life -= 1
            if self.board[y][x].life == 0:
                print('-' * 20)
                print('Убил.')
                print('-' * 20)
                self.count += 1
            else:
                print('-' * 20)
                print('Ранил.')
                print('-' * 20)
            self.board[y][x] = 2
    def ai(self):
        x = rnd(1, 6)
        y = rnd(1, 6)
        self.check_shot(x, y)
class Game:
    def __init__(self):
        self.ingame = True
        self.pl_board = Board()
        self.ai_board = Board()
        self.pl = GenerateShipSet(self.pl_board.board)
        self.ai = GenerateShipSet(self.ai_board.board)
        self.pl.start_gen()
        self.ai.start_gen()
        self.pl_shot = Shoot(self.ai_board.board)
        self.ai_shot = Shoot(self.pl_board.board)

    def gameLoop(self):
        while self.ingame:
            print('-' * 20)
            print('Ваше поле:')
            print('-' * 20)
            self.pl_board.print()
            print('-' * 20)
            print('Поле противника:')
            print('-' * 20)
            self.ai_board.print(True)
            print('Ходит Игрок.')
            print('-' * 20)
            self.pl_shot.player()
            if self.pl_shot.count == 7:
                print('-' * 20)
                print('-' * 20)
                print('-' * 20)
                print('Поздравляем вы победили!!!')
                break
            print('-' * 20)
            print('Ходит компьютер.')
            print('-' * 20)
            self.ai_shot.ai()
            if self.ai_shot.count == 7:
                print('-' * 20)
                print('-' * 20)
                print('-' * 20)
                print('Вы проиграли:(')
                break

g = Game()
g.gameLoop()
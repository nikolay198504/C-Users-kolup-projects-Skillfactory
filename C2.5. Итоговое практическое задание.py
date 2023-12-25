import random

# Исключения
class BoardOutException(Exception):
    pass

class ShipPlacementException(Exception):
    pass

class AlreadyShotException(Exception):
    pass

# Класс точки на поле
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Класс корабля
class Ship:
    def __init__(self, length, nose, direction):
        self.length = length
        self.nose = nose
        self.direction = direction
        self.lives = length

    def dots(self):
        ship_dots = []
        for i in range(self.length):
            x, y = self.nose.x, self.nose.y
            if self.direction == 'horizontal':
                ship_dots.append(Dot(x, y + i))
            else:
                ship_dots.append(Dot(x + i, y))
        return ship_dots

# Класс игровой доски
class Board:
    def __init__(self, hid=False):
        self.size = 6
        self.hid = hid
        self.field = [["O"] * self.size for _ in range(self.size)]
        self.ships = []
        self.alive = 0

    def add_ship(self, ship):
        for d in ship.dots():
            if self.out(d) or self.field[d.x][d.y] != "O":
                raise ShipPlacementException()
        for d in ship.dots():
            self.field[d.x][d.y] = "■"
            self.contour(d)
        self.ships.append(ship)
        self.alive += 1

    def contour(self, dot, verb=False):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cur = Dot(dot.x + dx, dot.y + dy)
                if not(self.out(cur)) and self.field[cur.x][cur.y] == "O":
                    if verb:
                        self.field[cur.x][cur.y] = "."

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, d):
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if self.field[d.x][d.y] in [".", "T", "X"]:
            raise AlreadyShotException()

        self.field[d.x][d.y] = "T"
        for ship in self.ships:
            if d in ship.dots():
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.alive -= 1
                    self.contour(ship.nose, True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        print("Мимо!")
        return False

# Класс игрока
class Player:
    def __init__(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardOutException:
                print("Выстрел за пределы поля!")
            except AlreadyShotException:
                print("Сюда уже стреляли!")

# Классы AI и User
class AI(Player):
    def ask(self):
        d = Dot(random.randint(0, 5), random.randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            move = input("Ваш ход (например, 23 для строки 2 и столбца 3): ")
            if len(move) != 2:
                print("Введите 2 координаты")
                continue
            x, y = move
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

# Класс игры
class Game:
    def __init__(self):
        pl = self.random_board()
        co = self.random_board(True)
        self.ai = AI(co, pl)
        self.user = User(pl, co)

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board()
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(l, Dot(random.randint(0, 5), random.randint(0, 5)), random.choice(['horizontal', 'vertical']))
                try:
                    board.add_ship(ship)
                    break
                except ShipPlacementException:
                    pass
        board.alive = len(lens)
        return board

    def random_board(self, hid=False):
        board = None
        while board is None:
            board = self.try_board()
        board.hid = hid
        return board

    def greet(self):
        print("-------------------")
        print("  Добро пожаловать  ")
        print("      в игру       ")
        print("    Морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.user.board)
            print("-" * 20)
            print("Доска компьютера:")
            # Временно отключаем скрытие кораблей на доске компьютера
            self.ai.board.hid = False
            print(self.ai.board)
            # Возвращаем настройку скрытия кораблей обратно
            self.ai.board.hid = True
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.alive == 0:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.user.board.alive == 0:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

if __name__ == "__main__":
    g = Game()
    g.start()

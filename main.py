import random

class Ship:
    def __init__(self, x, y, length, direction):
        self.x = x
        self.y = y
        self.length = length
        self.direction = direction
        self.hits = 0

    def hit(self):
        self.hits += 1

    def is_sunk(self):
        return self.hits == self.length

class Board:
    def __init__(self, size):
        self.size = size
        self.ships = []
        self.shots = []

    def add_ship(self, ship):
        for i in range(ship.length):
            if ship.direction == 'h':
                if ship.x + i >= self.size or (ship.y, ship.x + i) in self.ships:
                    raise Exception("Неправильное размещение судна")
            else:
                if ship.y + i >= self.size or (ship.y + i, ship.x) in self.ships:
                    raise Exception("Неправильное размещение судна")
        self.ships.append((ship.y, ship.x))
        self.ships.extend([(ship.y + i, ship.x) if ship.direction == 'v' else (ship.y, ship.x + i) for i in range(1, ship.length)])

    def shoot(self, x, y):
        if (y, x) in self.shots:
            raise Exception("Вы уже стреляли с этой позиции")
        self.shots.append((y, x))
        for ship in self.ships:
            if ship == (y, x):
                return 'Попадание!'
        return 'Промах!'

    def print_board(self):
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in range(self.size):
            print(f'{i+1} |', end='')
            for j in range(self.size):
                if (i+1, j+1) in self.shots:
                    if (i+1, j+1) in self.ships:
                        print(' X |', end='')
                    else:
                        print(' T |', end='')
                else:
                    print(' O |', end='')
            print()

class Game:
    def __init__(self):
        self.player_board = Board(6)
        self.ai_board = Board(6)
        self.player_ships = [Ship(0, 0, 3, 'h'), Ship(0, 0, 2, 'h'), Ship(0, 0, 2, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h')]
        self.ai_ships = [Ship(0, 0, 3, 'h'), Ship(0, 0, 2, 'h'), Ship(0, 0, 2, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h'), Ship(0, 0, 1, 'h')]

    def place_ships(self):
        for ship in self.player_ships:
            while True:
                ship.x = random.randint(0, 5)
                ship.y = random.randint(0, 5)
                ship.direction = random.choice(['h', 'v'])
                try:
                    self.player_board.add_ship(ship)
                    break
                except Exception as e:
                    pass
        for ship in self.ai_ships:
            while True:
                ship.x = random.randint(0, 5)
                ship.y = random.randint(0, 5)
                ship.direction = random.choice(['h', 'v'])
                try:
                    self.ai_board.add_ship(ship)
                    break
                except Exception as e:
                    pass

    def play(self):
        self.place_ships()
        while True:
            self.player_board.print_board()
            x, y = map(int, input("Введите координаты вашего снимка (x, y): ").split())
            result = self.ai_board.shoot(x-1, y-1)
            print(result)
            if all(ship.is_sunk() for ship in self.ai_ships):
                print("Ты победил!")
                break
            ai_x = random.randint(0, 5)
            ai_y = random.randint(0, 5)
            while (ai_y, ai_x) in self.player_board.shots:
                ai_x = random.randint(0, 5)
                ai_y = random.randint(0, 5)
            result = self.player_board.shoot(ai_x, ai_y)
            print(result)
            if all(ship.is_sunk() for ship in self.player_ships):
                print("Победил ИИ!")
                break

game = Game()
game.play()
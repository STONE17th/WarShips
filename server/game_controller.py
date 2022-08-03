
class Ship():
    def __init__(self, size, direct, x, y, id):
        self.id = id
        self.size = size
        self.direct = direct
        self.x = x
        self.y = y
        self.init_cells()

    def dump(self):
        return (self.size, self.direct, self.x, self.y)
        
    def coords(self):
        return (self.x, self.y)
    
    def init_cells(self):
        self.cells = set()
        for i in range(self.size):            
            if self.direct == 0: 
                self.cells.add((self.x + i, self.y))
            else: 
                self.cells.add((self.x, self.y + i))
            

class Field():
    def __init__(self, ships):
        self.field = {}
        for elem in ships:
            for cell in elem.cells:
                self.field[cell] = elem.id


class Game():
    id = 0
    def __init__(self, player1, player2):
        Game.id += 1
        self.id = Game.id
        self.turn = player1
        self.players = [player1, player2]
        self.enemy = {}
        self.enemy[player1] = player2
        self.enemy[player2] = player1
        self.score = {}
        self.score[player1] = 0
        self.score[player2] = 0
        self.players_ships = {}
        self.players_fields = {}
    


def get_ships(data: bytearray) -> list:
    id = 0
    ships = []
    for i in range(1,len(data),4):
        ships.append(Ship(data[i], data[i+1], data[i+2], data[i+3], id))
        id += 1
    return ships


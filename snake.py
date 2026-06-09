from enum import Enum
from PyQt5.QtCore import Qt
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    
STEROWANIE_G1= {
    Qt.Key_W: Direction.UP,
    Qt.Key_S: Direction.DOWN,
    Qt.Key_A: Direction.LEFT,
    Qt.Key_D: Direction.RIGHT
}


STEROWANIE_G2 = {
    Qt.Key_Up: Direction.UP,
    Qt.Key_Down: Direction.DOWN,
    Qt.Key_Left: Direction.LEFT,
    Qt.Key_Right: Direction.RIGHT
}

class Segment:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, inny):
        if not isinstance(inny, Segment):
            return False
        return self.x == inny.x and self.y == inny.y

    def getPosition(self):
        return self.x, self.y

class Snake:
    def __init__(self, x: int, y: int, player_id: int = 1, color: str = "Neon"):
        self.direction = Direction.RIGHT if player_id == 1 else Direction.LEFT
        
        if self.direction == Direction.RIGHT:
            self.body = [Segment(x, y), Segment(x - 1, y)]
        else:
            self.body = [Segment(x, y), Segment(x + 1, y)]
        self.score = 0
        self.speed = 10
        self.color = color
        self.playerId = player_id
        self.boostActive = False
        self.boostDuration = 0

    @property
    def glowa(self):
        return self.body[0]

    def move(self):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y
        if self.direction == Direction.UP:
            nowy_y -= 1
        elif self.direction == Direction.DOWN:
            nowy_y += 1
        elif self.direction == Direction.LEFT:
            nowy_x -= 1
        elif self.direction == Direction.RIGHT:
            nowy_x += 1

        self.body.insert(0, Segment(nowy_x, nowy_y))
        self.body.pop()

    def grow(self, bonus_predkosci: int = 1):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y

        if self.direction == Direction.UP:
            nowy_y -= 1
        elif self.direction == Direction.DOWN:
            nowy_y += 1
        elif self.direction == Direction.LEFT:
            nowy_x -= 1
        elif self.direction == Direction.RIGHT:
            nowy_x += 1

        self.body.insert(0, Segment(nowy_x, nowy_y))
        self.score += 1
        if self.boostActive:
            self.speed += bonus_predkosci

    def zmien_kierunek(self, nowy_kierunek: Direction):
        if nowy_kierunek == Direction.UP and self.direction != Direction.DOWN:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.DOWN and self.direction != Direction.UP:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = nowy_kierunek

    def checkSelfHit(self) -> bool:
        return self.glowa in self.body[1:]

    def activateBoost(self, duration: int):
        self.boostActive = True
        self.boostDuration = duration

    def deactivateBoost(self):
        self.boostActive = False
        self.boostDuration = 0

class InputHandler:
    def __init__(self):
        self.uklady = {
            1: STEROWANIE_G1,        
            2: STEROWANIE_G2
        }

    def readAndSendInput(self, event_key, snakes: list):
        for player_id, klawisze in self.uklady.items():
            if event_key in klawisze:
                nowy_kierunek = klawisze[event_key]
                for waz in snakes:
                    if waz.playerId == player_id:
                        waz.zmien_kierunek(nowy_kierunek)
                        return
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
        self.direction = Direction.UP if player_id == 1 else Direction.DOWN
        
        if self.direction == Direction.UP:
            self.body = [Segment(x, y), Segment(x, y + 1)]
        else:
            self.body = [Segment(x, y), Segment(x, y - 1)]
        self.score = 0
        self.speed = 10
        self.color = color
        self.playerId = player_id
        self.boostActive = False
        self.boostDuration = 0
        self.manualBoost = False

    @property
    def glowa(self):
        return self.body[0]

    def move(self, nowy_x: int, nowy_y: int, zjedzono_owoc: bool = False):
        """Przemieszcza węża na współrzędne podane bezpośrednio z silnika gry."""
        self.body.insert(0, Segment(nowy_x, nowy_y))
        
        if zjedzono_owoc:
            self.score += 1
            
        else:
            self.body.pop() 
        

    def zmien_kierunek(self, nowy_kierunek: Direction):
        if nowy_kierunek == Direction.UP and self.direction != Direction.DOWN:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.DOWN and self.direction != Direction.UP:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = nowy_kierunek
    
    def ręczne_przyspieszenie(self):
        """Przełącza stan ręcznego przyspieszenia."""
        self.manualBoost = not self.manualBoost

    def resetuj_przyspieszenia(self):
        """Wyłącza wszystkie efekty przyspieszenia (np. po zjedzeniu owocu)."""
        self.manualBoost = False
        self.boostActive = False
        self.boostDuration = 0

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
        self.przyspieszenie_klawisze = {
            Qt.Key_Q: 1,          
            Qt.Key_Space: 2       
        }

    def readAndSendInput(self, event_key, snakes: list):
        if event_key in self.przyspieszenie_klawisze:
            p_id = self.przyspieszenie_klawisze[event_key]
            for waz in snakes:
                if waz.playerId == p_id:
                    waz.ręczne_przyspieszenie()
                    return True

        for player_id, klawisze in self.uklady.items():
            if event_key in klawisze:
                nowy_kierunek = klawisze[event_key]
                for waz in snakes:
                    if waz.playerId == player_id:
                        waz.zmien_kierunek(nowy_kierunek)
                        return True
        return False
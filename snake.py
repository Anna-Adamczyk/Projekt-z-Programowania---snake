from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, inny):
        if not isinstance(inny, Segment):
            return False
        return self.x == inny.x and self.y == inny.y

class Snake:
    def __init__(self, x, y, rozmiar_bloku=20):
        self.body = [Segment(x, y), Segment(x - rozmiar_bloku, y)]
        self.direction = Direction.RIGHT 
        self.rozmiar_bloku = rozmiar_bloku
        self.score = 0
        self.speed = 10

    @property
    def glowa(self):
        return self.body[0]

    def move(self):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y
        if self.direction == Direction.UP:
            nowy_y -= self.rozmiar_bloku
        elif self.direction == Direction.DOWN:
            nowy_y += self.rozmiar_bloku
        elif self.direction == Direction.LEFT:
            nowy_x -= self.rozmiar_bloku
        elif self.direction == Direction.RIGHT:
            nowy_x += self.rozmiar_bloku

        self.body.insert(0, Segment(nowy_x, nowy_y))
        self.body.pop()

    def grow(self, bonus_predkosci):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y

        if self.direction == Direction.UP:
            nowy_y -= self.rozmiar_bloku
        elif self.direction == Direction.DOWN:
            nowy_y += self.rozmiar_bloku
        elif self.direction == Direction.LEFT:
            nowy_x -= self.rozmiar_bloku
        elif self.direction == Direction.RIGHT:
            nowy_x += self.rozmiar_bloku

        self.body.insert(0, Segment(nowy_x, nowy_y))
        self.score += 1
        self.speed += bonus_predkosci

    def zmien_kierunek(self, nowy_kierunek):
        if nowy_kierunek == Direction.UP and self.direction != Direction.DOWN:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.DOWN and self.direction != Direction.UP:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = nowy_kierunek

    def checkSelfHit(self):
        return self.glowa in self.body[1:]


class InputHandler:
    def __init__(self, klawisz_gora, klawisz_dol, klawisz_lewo, klawisz_prawo):
        self.klawisze = {
            klawisz_gora: Direction.UP,
            klawisz_dol: Direction.DOWN,
            klawisz_lewo: Direction.LEFT,
            klawisz_prawo: Direction.RIGHT
        }

    def obsluz_wejscie(self, waz, wcisniety_klawisz):
        if wcisniety_klawisz in self.klawisze:
            nowy_kierunek = self.klawisze[wcisniety_klawisz]
            waz.zmien_kierunek(nowy_kierunek)

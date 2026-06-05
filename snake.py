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
        self.cialo = [Segment(x, y), Segment(x - rozmiar_bloku, y)]
        self.kierunek = Direction.RIGHT 
        self.rozmiar_bloku = rozmiar_bloku
        self.wynik = 0
        self.predkosc = 10

    @property
    def glowa(self):
        return self.cialo[0]

    def sterowanie(self):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y
        if self.kierunek == Direction.UP:
            nowy_y -= self.rozmiar_bloku
        elif self.kierunek == Direction.DOWN:
            nowy_y += self.rozmiar_bloku
        elif self.kierunek == Direction.LEFT:
            nowy_x -= self.rozmiar_bloku
        elif self.kierunek == Direction.RIGHT:
            nowy_x += self.rozmiar_bloku

        self.cialo.insert(0, Segment(nowy_x, nowy_y))
        self.cialo.pop()

    def rosnij(self, bonus_predkosci):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y

        if self.kierunek == Direction.UP:
            nowy_y -= self.rozmiar_bloku
        elif self.kierunek == Direction.DOWN:
            nowy_y += self.rozmiar_bloku
        elif self.kierunek == Direction.LEFT:
            nowy_x -= self.rozmiar_bloku
        elif self.kierunek == Direction.RIGHT:
            nowy_x += self.rozmiar_bloku

        self.cialo.insert(0, Segment(nowy_x, nowy_y))
        self.wynik += 1
        self.predkosc += bonus_predkosci

    def zmien_kierunek(self, nowy_kierunek):
        if nowy_kierunek == Direction.UP and self.kierunek != Direction.DOWN:
            self.kierunek = nowy_kierunek
        elif nowy_kierunek == Direction.DOWN and self.kierunek != Direction.UP:
            self.kierunek = nowy_kierunek
        elif nowy_kierunek == Direction.LEFT and self.kierunek != Direction.RIGHT:
            self.kierunek = nowy_kierunek
        elif nowy_kierunek == Direction.RIGHT and self.kierunek != Direction.LEFT:
            self.kierunek = nowy_kierunek

    def checkSelfHit(self):
        return self.glowa in self.cialo[1:]


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

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, inny):
        return self.x == inny.x and self.y == inny.y

class Snake:
    def __init__(self, x, y, rozmiar_bloku=20):
        self.cialo = [Segment(x, y)]
        self.kierunek = "PRAWO" 
        self.rozmiar_bloku = rozmiar_bloku
        self.wynik = 0
        self.predkosc = 10

    @property
    def glowa(self):
        return self.cialo[0]

    def sterowanie(self):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y
        if self.kierunek == "GORA":
            nowy_y -= self.rozmiar_bloku
        elif self.kierunek == "DOL":
            nowy_y += self.rozmiar_bloku
        elif self.kierunek == "LEWO":
            nowy_x -= self.rozmiar_bloku
        elif self.kierunek == "PRAWO":
            nowy_x += self.rozmiar_bloku

        self.cialo.insert(0, Segment(nowy_x, nowy_y))
        self.cialo.pop()

    def rosnij(self, bonus_predkosci):
        nowy_x, nowy_y = self.glowa.x, self.glowa.y

        if self.kierunek == "GORA":
            nowy_y -= self.rozmiar_bloku
        elif self.kierunek == "DOL":
            nowy_y += self.rozmiar_bloku
        elif self.kierunek == "LEWO":
            nowy_x -= self.rozmiar_bloku
        elif self.kierunek == "PRAWO":
            nowy_x += self.rozmiar_bloku

        self.cialo.insert(0, Segment(nowy_x, nowy_y))
        self.wynik += 1
        self.predkosc += bonus_predkosci

    def zmien_kierunek(self, nowy_kierunek):
        if nowy_kierunek == "GORA" and self.kierunek != "DOL":
            self.kierunek = nowy_kierunek
        elif nowy_kierunek == "DOL" and self.kierunek != "GORA":
            self.kierunek = nowy_kierunek
        elif nowy_kierunek == "LEWO" and self.kierunek != "PRAWO":
            self.kierunek = nowy_kierunek
        elif nowy_kierunek == "PRAWO" and self.kierunek != "LEWO":
            self.kierunek = nowy_kierunek


import pygame

class InputHandler:
    def __init__(self, klawisz_gora, klawisz_dol, klawisz_lewo, klawisz_prawo):
        self.klawisze = {
            klawisz_gora: "GORA",
            klawisz_dol: "DOL",
            klawisz_lewo: "LEWO",
            klawisz_prawo: "PRAWO"
        }

    def obsluz_wejscie(self, waz, wcisniety_klawisz):
        if wcisniety_klawisz in self.klawisze:
            nowy_kierunek = self.klawisze[wcisniety_klawisz]
            waz.zmien_kierunek(nowy_kierunek)
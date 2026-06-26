from enum import Enum
from typing import List, Dict, Tuple, Union, Optional
from PyQt5.QtCore import Qt

class Direction(Enum):
    """Reprezentuje możliwe kierunki ruchu węża."""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


# Mapowanie klawiszy dla Gracza 1 (WSAD)
STEROWANIE_G1: Dict[int, Direction] = {
    Qt.Key_W: Direction.UP,
    Qt.Key_S: Direction.DOWN,
    Qt.Key_A: Direction.LEFT,
    Qt.Key_D: Direction.RIGHT
}

# Mapowanie klawiszy dla Gracza 2 (Strzałki)
STEROWANIE_G2: Dict[int, Direction] = {
    Qt.Key_Up: Direction.UP,
    Qt.Key_Down: Direction.DOWN,
    Qt.Key_Left: Direction.LEFT,
    Qt.Key_Right: Direction.RIGHT
}


class Segment:
    """Reprezentuje pojedynczy segment (część ciała) węża na planszy."""

    def __init__(self, x: int, y: int) -> None:
        """
        Inicjalizuje segment na podanych współrzędnych.

        :param x: Pozycja pozioma segmentu.
        :param y: Pozycja pionowa segmentu.
        """
        self.x: int = x
        self.y: int = y

    def __eq__(self, inny: object) -> bool:
        """
        Sprawdza, czy dwa segmenty mają te same współrzędne.

        :param inny: Obiekt do porównania.
        :return: True, jeśli obiekty są segmentami o identycznych współrzędnych, w przeciwnym razie False.
        """
        if not isinstance(inny, Segment):
            return False
        return self.x == inny.x and self.y == inny.y

    def getPosition(self) -> Tuple[int, int]:
        """
        Zwraca aktualną pozycję segmentu.

        :return: Krotka (x, y) reprezentująca współrzędne.
        """
        return self.x, self.y


class Snake:
    """Reprezentuje węża sterowanego przez gracza, przechowuje jego stan, pozycję i statystyki."""

    def __init__(self, x: int, y: int, player_id: int = 1, color: str = "Neon") -> None:
        """
        Inicjalizuje obiekt węża ze startową pozycją i domyślnymi parametrami.

        :param x: Początkowa współrzędna X głowy węża.
        :param y: Początkowa współrzędna Y głowy węża.
        :param player_id: Identyfikator gracza (1 lub 2).
        :param color: Nazwa koloru/skórki węża.
        """
        self.playerId: int = player_id
        self.color: str = color
        
        # Określenie domyślnego kierunku w zależności od gracza
        self.direction: Direction = Direction.UP if player_id == 1 else Direction.DOWN
        
        # Tworzenie początkowego dwu-segmentowego ciała w zależności od kierunku
        if self.direction == Direction.UP:
            self.body: List[Segment] = [Segment(x, y), Segment(x, y + 1)]
        else:
            self.body: List[Segment] = [Segment(x, y), Segment(x, y - 1)]
            
        self.score: int = 0
        self.speed: int = 10
        self.boostActive: bool = False
        self.boostDuration: int = 0
        self.manualBoost: bool = False

    @property
    def glowa(self) -> Segment:
        """
        Zwraca segment reprezentujący głowę węża.

        :return: Pierwszy element z listy segmentów ciała.
        """
        return self.body[0]

    def move(self, nowy_x: int, nowy_y: int, zjedzono_owoc: bool = False) -> None:
        """
        Przemieszcza węża na nowe współrzędne podane z silnika gry.

        Dodaje nowy segment na początku ciała. Jeśli wąż nie zjadł owocu, 
        usuwany jest ostatni segment ciała (efekt ruchu).

        :param nowy_x: Nowa współrzędna X dla głowy węża.
        :param nowy_y: Nowa współrzędna Y dla głedy węża.
        :param zjedzono_owoc: Flaga informująca, czy w tej turze wąż zdobył punkt (wtedy rośnie).
        """
        self.body.insert(0, Segment(nowy_x, nowy_y))
        
        if zjedzono_owoc:
            self.score += 1
        else:
            self.body.pop()

    def zmien_kierunek(self, nowy_kierunek: Direction) -> None:
        """
        Zmienia aktualny kierunek ruchu węża, blokując możliwość natychmiastowego zwrotu o 180 stopni.

        :param nowy_kierunek: Kierunek, w którym wąż ma zacząć się poruszać.
        """
        if nowy_kierunek == Direction.UP and self.direction != Direction.DOWN:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.DOWN and self.direction != Direction.UP:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = nowy_kierunek
        elif nowy_kierunek == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = nowy_kierunek
    
    def ręczne_przyspieszenie(self) -> None:
        """Przełącza stan ręcznego przyspieszenia (włącza/wyłącza)."""
        self.manualBoost = not self.manualBoost

    def resetuj_przyspieszenia(self) -> None:
        """Wyłącza wszystkie efekty przyspieszenia (np. wywoływane po zjedzeniu owocu)."""
        self.manualBoost = False
        self.boostActive = False
        self.boostDuration = 0

    def checkSelfHit(self) -> bool:
        """
        Sprawdza, czy głowa węża zderzyła się z jakąkolwiek częścią jego własnego ciała.

        :return: True, jeśli doszło do kolizji ze samym sobą, w przeciwnym razie False.
        """
        return self.glowa in self.body[1:]

    def activateBoost(self, duration: int) -> None:
        """
        Aktywuje czasowe przyspieszenie (np. z power-upa).

        :param duration: Czas trwania lub liczba kroków, przez które przyspieszenie ma działać.
        """
        self.boostActive = True
        self.boostDuration = duration

    def deactivateBoost(self) -> None:
        """Natychmiastowo wyłącza czasowe przyspieszenie i zeruje jego licznik."""
        self.boostActive = False
        self.boostDuration = 0


class InputHandler:
    """Klasa odpowiedzialna za przechwytywanie zdarzeń klawiatury i sterowanie odpowiednimi wężami."""

    def __init__(self) -> None:
        """Inicjalizuje układy sterowania oraz klawisze funkcyjne (przyspieszenia) dla graczy."""
        self.uklady: Dict[int, Dict[int, Direction]] = {
            1: STEROWANIE_G1,        
            2: STEROWANIE_G2
        }
        self.przyspieszenie_klawisze: Dict[int, int] = {
            Qt.Key_Q: 1,          
            Qt.Key_Space: 2       
        }

    def readAndSendInput(self, event_key: int, snakes: List[Snake]) -> bool:
        """
        Odczytuje wciśnięty klawisz i przekazuje odpowiednią akcję (ruch lub dopalacz) właściwemu wężowi.

        :param event_key: Kod wciśniętego klawisza (z biblioteki PyQt5).
        :param snakes: Lista aktywnych obiektów klasy Snake w grze.
        :return: True, jeśli klawisz został obsłużony przez system sterowania, w przeciwnym razie False.
        """
        # Sprawdzenie klawiszy odpowiedzialnych za przyspieszenie
        if event_key in self.przyspieszenie_klawisze:
            p_id = self.przyspieszenie_klawisze[event_key]
            for waz in snakes:
                if waz.playerId == p_id:
                    waz.ręczne_przyspieszenie()
                    return True

        # Sprawdzenie klawiszy odpowiedzialnych za zmianę kierunku ruchu
        for player_id, klawisze in self.uklady.items():
            if event_key in klawisze:
                nowy_kierunek = klawisze[event_key]
                for waz in snakes:
                    if waz.playerId == player_id:
                        waz.zmien_kierunek(nowy_kierunek)
                        return True
                        
        return False
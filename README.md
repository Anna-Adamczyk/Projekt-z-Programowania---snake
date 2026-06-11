# Snake Game – Dokumentacja projektu

## Autorzy 
Anna Adamczyk, Aleksandra Bród, Emilia Iluk, Magdalena Jankowiak, Zofia Szafran

Projekt został wykonany w ramach zajęć z programowania.

## Opis projektu

Snake Game jest grą napisaną w języku Python z wykorzystaniem biblioteki PyQt5. Gracz steruje wężem poruszającym się po planszy i zdobywa punkty poprzez zbieranie owoców. Gra obsługuje tryb jednoosobowy oraz wieloosobowy.

## Wymagania
python 
## Wymagane biblioteki

Biblioteki zewnętrzne:
- PyQt5

Biblioteki standardowe Pythona:
- sys
- random
- enum

## Instalacja(wpisz w terminalu)

1. Sklonuj repozytorium:

git clone (https://github.com/Anna-Adamczyk/Projekt-z-Programowania---snake.git)

2. Przejdź do katalogu projektu:

cd Projekt-z-Programowania---snake

3. Utwórz środowisko wirtualne:

python -m venv venv

4. Aktywuj środowisko:

Windows (Git Bash):

source venv/Scripts/activate

5. Zainstaluj wymagane biblioteki:

pip install PyQt5

6.Urochomienie

python GUI.py

## Cel gry

Celem gry jest zdobycie jak największej liczby punktów poprzez zbieranie owoców pojawiających się na planszy. Każdy zjedzony owoc powoduje wzrost długości węża oraz zwiększenie wyniku.

## Rozpoczęcie gry
Uruchom program.
W menu głównym wybierz:
tryb jednoosobowy lub multiplayer,
skórkę węża,
typ planszy,
dodatkowe opcje gry.
Kliknij przycisk „GRAJ”.
## Sterowanie
Gracz 1
W – ruch w górę
S – ruch w dół
A – ruch w lewo
D – ruch w prawo
Gracz 2 (tryb multiplayer)
↑ – ruch w górę
↓ – ruch w dół
← – ruch w lewo
→ – ruch w prawo
## Dostępne opcje
## Multiplayer

Umożliwia rozgrywkę dla dwóch graczy na jednej planszy.

## Magiczne owoce

Włącza możliwość pojawiania się specjalnych owoców zapewniających dodatkowe bonusy.

## Wall Pass

Pozwala przechodzić przez krawędzie planszy. Po opuszczeniu planszy z jednej strony wąż pojawia się po stronie przeciwnej.

## Wybór planszy

Dostępne są trzy rodzaje plansz:

Arena
Rectangle
Maze
Zasady przegranej

## Gra kończy się, gdy:

wąż uderzy w ścianę (jeśli opcja Wall Pass jest wyłączona),
wąż uderzy w przeszkodę,
wąż zderzy się z własnym ciałem,
w trybie multiplayer wąż zderzy się z drugim graczem.
## Punktacja

Za każdy zjedzony owoc gracz otrzymuje punkt. Aktualny wynik jest wyświetlany podczas rozgrywki na górze okna gry.

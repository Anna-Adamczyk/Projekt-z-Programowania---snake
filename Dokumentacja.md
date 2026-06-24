# Dokumentacja projektu – Snake Game

## 1. Opis projektu

Snake Game jest grą napisaną w języku Python z wykorzystaniem biblioteki PyQt5. Celem gracza jest sterowanie wężem, zbieranie owoców oraz zdobywanie jak największej liczby punktów. Gra obsługuje tryb jednoosobowy oraz wieloosobowy i oferuje dodatkowe opcje rozgrywki, takie jak przechodzenie przez ściany oraz magiczne owoce zwiększające prędkość poruszania się węża.

---

# 2. Instrukcja uruchomienia

## Wymagania

* Python 3.10 lub nowszy
* Git (opcjonalnie, do pobrania projektu)

## Instalacja projektu

1. Sklonuj repozytorium:

```bash
git clone https://github.com/Anna-Adamczyk/Projekt-z-Programowania---snake.git
```

2. Przejdź do katalogu projektu:

```bash
cd Projekt-z-Programowania---snake
```

3. Utwórz środowisko wirtualne:

```bash
python -m venv venv
```

4. Aktywuj środowisko:

Windows (Git Bash):

```bash
source venv/Scripts/activate
```

Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

5. Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

6. Uruchom program:

```bash
python GUI.py
```

---

# 3. Lista wymaganych bibliotek

Projekt wykorzystuje następujące biblioteki:

* PyQt5
* random (biblioteka standardowa Pythona)
* enum (biblioteka standardowa Pythona)
* sys (biblioteka standardowa Pythona)

---

# 4. Instrukcja użytkownika

Po uruchomieniu programu wyświetla się menu główne.

Użytkownik może:

* rozpocząć grę,
* włączyć lub wyłączyć tryb Multiplayer,
* włączyć lub wyłączyć Magic Fruit,
* włączyć lub wyłączyć Wall Pass,
* wybrać skórkę węża,
* wybrać rodzaj planszy.

## Sterowanie

### Gracz 1

* W – ruch w górę
* A – ruch w lewo
* S – ruch w dół
* D – ruch w prawo

### Gracz 2

* Strzałka ↑ – ruch w górę
* Strzałka ← – ruch w lewo
* Strzałka ↓ – ruch w dół
* Strzałka → – ruch w prawo

## Cel gry

Celem gry jest zdobycie jak największej liczby punktów poprzez zbieranie owoców.

Gra kończy się, gdy:

* wąż uderzy w ścianę (jeżeli opcja Wall Pass jest wyłączona),
* wąż uderzy w przeszkodę,
* wąż uderzy we własne ciało,
* w trybie wieloosobowym nastąpi kolizja z drugim wężem.

---

# 5. Opis funkcjonalności

### Food

Standardowy owoc zwiększający wynik gracza o 1 punkt.

### Magic Fruit

Specjalny owoc zwiększający prędkość poruszania się węża na około 3 sekundy.

### Wall Pass

Po włączeniu tej opcji wąż może przechodzić przez krawędzie planszy bez zakończenia gry.

### Multiplayer

Gra umożliwia jednoczesną rozgrywkę dwóch graczy.

### Wybór planszy

Dostępne są trzy rodzaje plansz:

* Arena
* Rectangle
* Maze

### Wybór skórki

Gracz może wybrać jedną z dostępnych skórek węża:

* Neon
* Fire
* Ice

---

# 6. Diagram klas UML


---

# 7. Zaktualizowany plan funkcjonalności

## Zrealizowane funkcjonalności

* menu główne,
* tryb jednoosobowy,
* tryb wieloosobowy,
* wybór planszy,
* wybór skórki,
* licznik punktów,
* zwykły owoc (Food),
* magiczny owoc (Magic Fruit),
* czasowe zwiększenie prędkości po zjedzeniu Magic Fruit,
* Wall Pass,
* wykrywanie kolizji,
* ekran zakończenia gry.


---

# 8. Struktura projektu

```
Projekt-z-Programowania---snake
│
├── GUI.py
├── board.py
├── snake.py
├── fruit.py
├── game.py
├── main.py
├── requirements.txt
├── README.md
├── diagram UML.png
└── Dokumentacja.md
```

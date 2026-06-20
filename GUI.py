import random
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QCheckBox,
    QStackedLayout, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer
from board import Board, Difficulty, BoardShape
from snake import Snake, Direction, InputHandler
from fruit import Food, MagicFruit


# ================= GAME CANVAS =================
class GameCanvas(QWidget):
    """"Obsługa gry (planszy, węży, owoców, ulepszeń)"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedSize(650, 420)

        self.setFocusPolicy(Qt.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)

        self.board = None
        self.snakes = []
        self.difficulty = None
        self.input_handler = InputHandler()
        self.food = None
        self.magic_fruit = None
        self.normal_speed = 150

    def get_tile_widget(self, x, y):
        """Pobiera konkretny widżet kafelka QLabel z układu siatki (QGridLayout)."""
        layout = self.layout()
        if layout:
            item = layout.itemAtPosition(y, x)
            if item and item.widget():
                return item.widget()
        return None

    def startGame(self):
        """Rozpoczyna grę."""
        wyksztalt = BoardShape[self.parent.chosen_board]
        self.difficulty = Difficulty(level=1, snake_speed=150, board_shape=wyksztalt)
        self.board = Board(20, 20, self.difficulty)

        self.snakes = []
        
        # Gracz 1
        g1 = Snake(5, 10, player_id=1, color=self.parent.skin)
        if self.parent.control_p1 == "Strzałki":
            g1.playerId = 2  
        else:
            g1.playerId = 1  
        self.snakes.append(g1)
        
        # Gracz 2 (Multiplayer)
        if self.parent.multi:
            kolor_g2 = "Fire" if self.parent.skin != "Fire" else "Ice"
            g2 = Snake(14, 6, player_id=2, color=kolor_g2)
            if self.parent.control_p1 == "Strzałki":
                g2.playerId = 1  
            else:
                g2.playerId = 2  
            self.snakes.append(g2)

        # Rysowanie planszy za pomocą metody z board.py
        self.board.init_display(self)

        # Inicjalizacja owoców
        self.food = Food()
        self.food.spawn(self.board)

        if self.parent.magic:
            self.magic_fruit = MagicFruit()
            self.magic_fruit.spawn(self.board)
        else:
            self.magic_fruit = None

        self.timer.start(self.normal_speed)
        self.setFocus()

    def keyPressEvent(self, event):
        """Odpowiada za obsługę ruchu."""
        klawisz = event.key()
        self.input_handler.readAndSendInput(klawisz, self.snakes)

    def game_loop(self):
        """Wykonuje raz główną pętlę gry."""
        if not self.snakes:
            return
        
        boost_active = any(w.boostActive or w.manualBoost for w in self.snakes)
        if boost_active:
            self.timer.setInterval(70)
        else:
            self.timer.setInterval(self.normal_speed)

        for waz in self.snakes:
            nastepny_x, nastepny_y = waz.glowa.x, waz.glowa.y
            if waz.direction == Direction.UP: nastepny_y -= 1
            elif waz.direction == Direction.DOWN: nastepny_y += 1
            elif waz.direction == Direction.LEFT: nastepny_x -= 1
            elif waz.direction == Direction.RIGHT: nastepny_x += 1

            if self.parent.wall_pass:
                if nastepny_x < 0: nastepny_x = self.board.width - 1
                elif nastepny_x >= self.board.width: nastepny_x = 0
                if nastepny_y < 0: nastepny_y = self.board.height - 1
                elif nastepny_y >= self.board.height: nastepny_y = 0

            pozycja_nastepna = (nastepny_x, nastepny_y)
            zwykly_zjedzony = (pozycja_nastepna == self.food.getPosition())
            magiczny_zjedzony = (self.magic_fruit and pozycja_nastepna == self.magic_fruit.getPosition())

            # Ruch węża
            waz.move(
                nowy_x=nastepny_x,
                nowy_y=nastepny_y,
                zjedzono_owoc=(zwykly_zjedzony or magiczny_zjedzony)
            )
            
            if zwykly_zjedzony:
                waz.resetuj_przyspieszenia()  
                self.food.spawn(self.board)
                
            if magiczny_zjedzony:
                waz.resetuj_przyspieszenia()  
                self.magic_fruit.applyEffect(waz)
                waz.score += 2 
                
                QTimer.singleShot(
                    self.magic_fruit.boostTime * 1000,
                    lambda w=waz: w.deactivateBoost()
                )
                self.magic_fruit.spawn(self.board)

        self.checkCollision()
        self.render_game()
        
        if len(self.snakes) == 2:
            self.parent.hud.setText(f"G1 SCORE: {self.snakes[0].score} |  G2 SCORE: {self.snakes[1].score}")
        else:
            turbo_info = " [TURBO]" if self.snakes[0].manualBoost or self.snakes[0].boostActive else ""
            self.parent.hud.setText(f"SCORE: {self.snakes[0].score}{turbo_info}")

    def checkCollision(self):
        """Sprawdza czy doszło do zderzenia."""
        for waz in self.snakes:
            glowa = waz.glowa
            
            if not self.parent.wall_pass:
                if glowa.x < 0 or glowa.x >= self.board.width or glowa.y < 0 or glowa.y >= self.board.height:
                    self.endGame(przegrany_id=waz.playerId)
                    return

                if self.board.is_obstacle(glowa.x, glowa.y):
                    is_food = (glowa.x, glowa.y) == self.food.getPosition()
                    is_magic = self.magic_fruit and (glowa.x, glowa.y) == self.magic_fruit.getPosition()
                    
                    if not (is_food or is_magic):
                        self.endGame(przegrany_id=waz.playerId)
                        return
             
            if waz.checkSelfHit():
                self.endGame(przegrany_id=waz.playerId)
                return

            for inny_waz in self.snakes:
                if waz == inny_waz:
                    continue
                if glowa in inny_waz.body:
                    self.endGame(przegrany_id=waz.playerId)
                    return

    def render_game(self):
        """Dynamicznie aktualizuje kolory na kafelkach wygenerowanych przez board.py."""
        theme = self.parent.get_theme()
        matrix = self.board.drawBoard()
        
        for y in range(self.board.height):
            for x in range(self.board.width):
                tile = self.get_tile_widget(x, y)
                if tile:
                    if self.board.is_obstacle(x, y):
                        tile.setStyleSheet("background-color: #1c2331; border: 1px solid #2b364a;")
                    elif matrix[y][x] == "TILE_A":
                        tile.setStyleSheet(f"background-color: {theme['bg']};")
                    else:
                        tile.setStyleSheet(f"background-color: {theme['bg']}; border: 1px solid rgba(0, 0, 0, 0.4);")

        fx, fy = self.food.getPosition()
        tile_food = self.get_tile_widget(fx, fy)
        if tile_food:
            tile_food.setStyleSheet(f"background-color: {theme['food']}; border-radius: 5px;")

        if self.magic_fruit:
            mx, my = self.magic_fruit.getPosition()
            tile_magic = self.get_tile_widget(mx, my)
            if tile_magic:
                tile_magic.setStyleSheet(f"background-color: {theme['magic']}; border-radius: 5px;")

        for waz in self.snakes:
            if len(self.snakes) == 1:
                kolor_weza = theme['snake']
            else:
                kolor_weza = theme['snake'] if waz == self.snakes[0] else theme['enemy']
                
            for i, segment in enumerate(waz.body):
                tile_seg = self.get_tile_widget(segment.x, segment.y)
                if tile_seg:
                    if i == 0:
                        tile_seg.setStyleSheet(f"background-color: {kolor_weza}; border: 2px solid #ffffff;")
                    else:
                        tile_seg.setStyleSheet(f"background-color: {kolor_weza};")

    def endGame(self, przegrany_id=1):
        """Kończy rozgrywkę."""
        self.timer.stop()
        
        if len(self.snakes) == 2:
            wygrany_id = 2 if przegrany_id == self.snakes[0].playerId else 1
            tekst = f"🏆 WYGRYWA GRACZ {wygrany_id}! 🏆\n\nGratulacje dla zwycięzcy!"
        else:
            wynik = self.snakes[0].score if self.snakes else 0
            tekst = f"💥 Przegrana! 💥\n\nTwój końcowy wynik to: {wynik}"

        szablon_baneru = """
            QMessageBox { background-color: #1c2331; border: 2px solid #2b364a; }
            QLabel { color: #ffffff; font-size: 14px; }
            QPushButton { background-color: #238636; color: white; font-weight: bold; padding: 6px; border-radius: 5px; min-width: 120px; }
            QPushButton:hover { background-color: #2ea043; }
        """
        
        box = QMessageBox(self)
        box.setWindowTitle("Koniec Gry 🐍")
        box.setText(tekst)
        box.setIcon(QMessageBox.Information)
        box.setStyleSheet(szablon_baneru)
        
        btn_restart = QPushButton("Zagraj ponownie")
        btn_menu = QPushButton("Powrót do menu")  # Naprawiono tekst przycisku wyjścia
        
        box.addButton(btn_restart, QMessageBox.AcceptRole)
        box.addButton(btn_menu, QMessageBox.RejectRole)
        
        wynik_okna = box.exec_() 
        
        if wynik_okna == QMessageBox.AcceptRole or wynik_okna == 0:
            self.startGame()  
        else:
            self.parent.stack.setCurrentIndex(0)


# ================= MAIN APP =================
class SnakeApp(QWidget):
    """Główne okno aplikacji Snake."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🐍 Snake - Wersja z ulepszeniami")
        self.setFixedSize(800, 680)
        self.setStyleSheet("background-color:#0d1117;")

        # STATE
        self.multi = False
        self.magic = True
        self.wall_pass = False
        self.skin = "Neon"
        self.chosen_board = "ARENA"
        self.control_p1 = "Litery (WASD)"

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.menu_ui()
        self.game_ui()
        self.info_ui()
        self.authors_ui()

        self.stack.setCurrentIndex(0)

    def get_theme(self):
        """Ustala wariant kolorystyczny rozgrywki."""
        if self.skin == "Neon":
            return {
                "bg": "#050816",
                "snake": "#00ff9f",
                "enemy": "#00c8ff",
                "food": "#ff007f",
                "magic": "#c77dff"
            }
        if self.skin == "Fire":
            return {
                "bg": "#1a0f0f",
                "snake": "#ff4d00",
                "enemy": "#ff9900",
                "food": "#ff0000",
                "magic": "#ffcc00"
            }
        return {
            "bg": "#0b1b2b",
            "snake": "#00d4ff",
            "enemy": "#5aa9ff",
            "food": "#ffffff",
            "magic": "#66ffff"
        }

    # ================= MENU =================
    def menu_ui(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(4)  # Zmniejsza globalny odstęp między elementami w menu

        title = QLabel("🐍 SNAKE GAME")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:32px;color:#2ecc71;font-weight:bold;margin-bottom:2px;")
        layout.addWidget(title)

        # SETTINGS
        self.multi_cb = QCheckBox("🎮 Multiplayer (G2 otrzyma przeciwne klawisze)")
        self.magic_cb = QCheckBox("🍇 Magiczne owoce")
        self.wall_cb = QCheckBox("🌀 Wall Pass")
        self.magic_cb.setChecked(True)

        for c in [self.multi_cb, self.magic_cb, self.wall_cb]:
            c.setStyleSheet("color:white;padding:1px;font-size:14px;margin:0px;")
            layout.addWidget(c)

        # KAFELKI ROZWIJANE BEZ OGROMNYCH ODSTĘPÓW
        lbl_p1 = QLabel("🕹️ Sterowanie Gracz 1:")
        lbl_p1.setStyleSheet("color:#8b949e;font-weight:bold;margin:0px;padding:0px;")
        layout.addWidget(lbl_p1)
        
        self.p1_box = QComboBox()
        self.p1_box.addItems(["Litery (WASD)", "Strzałki"])
        layout.addWidget(self.p1_box)

        lbl_board = QLabel("🗺️ Wybór planszy:")
        lbl_board.setStyleSheet("color:#8b949e;font-weight:bold;margin:0px;padding:0px;")
        layout.addWidget(lbl_board)

        self.board_box = QComboBox()
        self.board_box.addItems(["ARENA", "RECTANGLE", "MAZE"])
        layout.addWidget(self.board_box)

        lbl_skin = QLabel("🎨 Wybór motywu:")
        lbl_skin.setStyleSheet("color:#8b949e;font-weight:bold;margin:0px;padding:0px;")
        layout.addWidget(lbl_skin)

        self.skin_box = QComboBox()
        self.skin_box.addItems(["Neon", "Fire", "Ice"])
        layout.addWidget(self.skin_box)

    
        for box in [self.p1_box, self.board_box, self.skin_box]:
            box.setStyleSheet("background:#21262d; color:white; padding:4px; border-radius:6px; margin:0px;")

        # PRZYCISKI GŁÓWNE
        play = QPushButton("▶ GRAJ")
        info = QPushButton("📖 INSTRUKCJA")
        authors = QPushButton("👨‍💻 OD AUTOREK")

        play.clicked.connect(self.start_game)
        info.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        authors.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        for b in [play, info, authors]:
            b.setStyleSheet("""
                QPushButton {
                    background:#238636; color:white; padding:8px;
                    border-radius:10px; font-weight:bold; margin-top:2px;
                }
                QPushButton:hover { background:#2ea043; }
            """)
            layout.addWidget(b)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ================= GAME =================
    def game_ui(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.hud = QLabel("SCORE: 0")
        self.hud.setStyleSheet("color:white;font-weight:bold;font-size:16px;")

        self.canvas = GameCanvas(self)

        back = QPushButton("⬅ MENU")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        back.setStyleSheet("background:#30363d; color:white; padding:8px; border-radius:8px;")

        layout.addWidget(self.hud)
        layout.addWidget(self.canvas)
        layout.addWidget(back)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ================= INFO =================
    def info_ui(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("✨👨‍💻 INSTRUKCJA 👩‍💻✨")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; color:#c77dff; font-weight:bold;")

        text = QLabel("""
    🐍 CEL: zbieraj owoce i rośnij
    🕹️ Sterowanie: wybierz klawisze dla Gracza 1 w menu. Drugi gracz otrzyma automatycznie drugi zestaw!
                                
    Dostępne Ulepszenia: 
            🎮 Multiplayer = gra dla 2 osób
            🍇 Magiczne owoce = zjedzenie magicznego owocu aktywuje czasowe przyspieszenie
            🌀 Wall Pass = przechodzenie przez ściany i krawędzie
            🎨 3 warianty kolorystyczne (Neon, Fire, Ice)
            🗺️ 3 kształty planszy (ARENA, RECTANGLE, MAZE)                    
""")
        text.setStyleSheet("color:white; font-size: 15px;")

        back = QPushButton("⬅ POWRÓT")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        back.setStyleSheet("background:#238636; color:white; padding:10px; border-radius:10px; font-weight:bold;")

        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(back)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ================= AUTHORS =================
    def authors_ui(self):
        page = QWidget()
        layout = QVBoxLayout()

        title = QLabel("✨👨‍💻 OD AUTOREK 👩‍💻✨")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px; color:#c77dff; font-weight:bold;")

        text = QLabel("""
🎮 Snake z ulepszeniami
💡 Inteligentny podział klawiszy WASD/Strzałki dla trybu wieloosobowego!
🚀 Projekt na zaliczenie Programowania
🐍 Dziękujemy za uruchomienie gry!
""")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("color:white; font-size: 16px;")

        back = QPushButton("⬅ POWRÓT")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        back.setStyleSheet("background:#238636; color:white; padding:10px; border-radius:10px; font-weight:bold;")

        layout.addWidget(title)
        layout.addWidget(text)
        layout.addWidget(back)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ================= START GAME =================
    def start_game(self):
        self.multi = self.multi_cb.isChecked()
        self.magic = self.magic_cb.isChecked()
        self.wall_pass = self.wall_cb.isChecked()
        self.skin = self.skin_box.currentText()
        self.chosen_board = self.board_box.currentText()
        self.control_p1 = self.p1_box.currentText()

        self.stack.setCurrentIndex(1)
        self.canvas.startGame()
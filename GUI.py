import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QCheckBox,
    QStackedLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from board import Board, Difficulty, BoardShape
from snake import Snake, Direction, InputHandler


# ================= GAME CANVAS =================
class GameCanvas(QWidget):
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
        self.is_running = False
        self.input_handler = InputHandler()

    def startGame(self):
        self.difficulty = Difficulty(level=1, snake_speed=150, board_shape=BoardShape.ARENA)
        self.board = Board(20, 20, self.difficulty)
        self.snakes = []
        # Gracz 1 
        self.snakes.append(Snake(5, 10, player_id=1, color=self.parent.skin))
        
        # Multiplayer 
        if self.parent.multi:
            kolor_g2 = "Fire" if self.parent.skin != "Fire" else "Ice"
            self.snakes.append(Snake(14, 10, player_id=2, color=kolor_g2))

        self.board.init_display(self)
        self.is_running = True
        self.timer.start(self.difficulty.getSpeed())
        self.setFocus()

    def keyPressEvent(self, event):
        klawisz = event.key()
        if not self.parent.multi:
            strzalki = {
                Qt.Key_Up: Direction.UP,
                Qt.Key_Down: Direction.DOWN,
                Qt.Key_Left: Direction.LEFT,
                Qt.Key_Right: Direction.RIGHT
            }
            if klawisz in strzalki:
                self.snakes[0].zmien_kierunek(strzalki[klawisz])
                return
        self.input_handler.readAndSendInput(klawisz, self.snakes)

    def game_loop(self):
        if not self.snakes:
            return 
        for waz in self.snakes:
            glowa = waz.glowa
            nastepny_x, nastepny_y = glowa.x, glowa.y

            if waz.direction == Direction.UP:
                nastepny_y -= 1
            elif waz.direction == Direction.DOWN:
                nastepny_y += 1
            elif waz.direction == Direction.LEFT:
                nastepny_x -= 1
            elif waz.direction == Direction.RIGHT:
                nastepny_x += 1
                
            if self.parent.wall_pass:
                if nastepny_x < 0: nastepny_x = self.board.width - 1
                elif nastepny_x >= self.board.width: nastepny_x = 0 
                if nastepny_y < 0: nastepny_y = self.board.height - 1
                elif nastepny_y >= self.board.height: nastepny_y = 0

                glowa.x = nastepny_x
                glowa.y = nastepny_y

            waz.move()

        self.checkCollision()
        self.render_game()
        
       
        if len(self.snakes) == 2:
            self.parent.hud.setText(f"G1 SCORE: {self.snakes[0].score}  |  G2 SCORE: {self.snakes[1].score}")
        else:
            self.parent.hud.setText(f"SCORE: {self.snakes[0].score}")

    def checkCollision(self):
        for waz in self.snakes:
            glowa = waz.glowa
            
            if not self.parent.wall_pass:
                if glowa.x < 0 or glowa.x >= self.board.width or glowa.y < 0 or glowa.y >= self.board.height:
                    self.endGame(przegrany_id=waz.playerId)
                    return
        
                if self.board.is_obstacle(glowa.x, glowa.y):
                    self.endGame(przegrany_id=waz.playerId)
                    return
             
            # Samozderzenie
            if waz.checkSelfHit():
                self.endGame(przegrany_id=waz.playerId)
                return

            # Zderzenie z drugim wężem (wjechanie w czyjś ogon/ciało)
            for inny_waz in self.snakes:
                if waz == inny_waz:
                    continue
                if glowa in inny_waz.body:
                    self.endGame(przegrany_id=waz.playerId)
                    return

    def render_game(self):
        if not self.board or not self.snakes or not self.layout():
            return
            
        theme = self.parent.get_theme()
        matrix = self.board.drawBoard()
        grid = self.layout()  
        for y in range(self.board.height):
            for x in range(self.board.width):
                item = grid.itemAtPosition(y, x)
                if item and item.widget():
                    tile = item.widget()
                    if self.board.is_obstacle(x, y):
                        tile.setStyleSheet("background-color: #1c2331; border: 1px solid #2b364a;")
                    elif matrix[y][x] == "TILE_A":
                        tile.setStyleSheet(f"background-color: {theme['bg']};")
                    else:
                        tile.setStyleSheet(f"background-color: {theme['bg']}; border: 1px solid rgba(0, 0, 0, 0.4);")
        
        for waz in self.snakes:
            if waz.color == "Neon": kolor_hex = "#00ff9f"
            elif waz.color == "Fire": kolor_hex = "#ff4d00"
            else: kolor_hex = "#00d4ff" # Ice
            
            for i, segment in enumerate(waz.body):
                if 0 <= segment.x < self.board.width and 0 <= segment.y < self.board.height:
                    item = grid.itemAtPosition(segment.y, segment.x)
                    if item and item.widget():
                        tile = item.widget()
                        if i == 0:
                            tile.setStyleSheet(f"background-color: {kolor_hex}; border: 2px solid #ffffff; border-radius: 4px;")
                        else:
                            tile.setStyleSheet(f"background-color: {kolor_hex}; border-radius: 2px;")

   
    def endGame(self, przegrany_id=1):
        self.timer.stop()
        self.is_running = False
        
        if len(self.snakes) == 2:
            
            wygrany_id = 2 if przegrany_id == 1 else 1
            tekst = f" WYGRYWA GRACZ {wygrany_id}! \n\nGratulacje dla zwycięzcy!"
        else:
            
            wynik = self.snakes[0].score if self.snakes else 0
            tekst = f"Przegrana!\n\nTwój końcowy wynik to: {wynik} "

        szablon_baneru= """
            QMessageBox {
                background-color: #1c2331;
                border: 2px solid #2b364a;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #238636;
                color: white;
                font-weight: bold;
                padding: 6px;
                border-radius: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2ea043;
            }
        """
        
        box = QMessageBox(self)
        box.setWindowTitle("Koniec Gry 🐍")
        box.setText(tekst)
        box.setIcon(QMessageBox.Information)
        box.setStyleSheet(szablon_baneru)
        box.exec_() 
        
        
        self.parent.stack.setCurrentIndex(0)

# ================= MAIN APP =================
class SnakeApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🐍 Snake - Final PyQt5 Edition")
        self.setFixedSize(800, 680)
        self.setStyleSheet("background-color:#0d1117;")

        # STATE
        self.multi = False
        self.magic = True
        self.wall_pass = False
        self.skin = "Neon"

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.menu_ui()
        self.game_ui()
        self.info_ui()
        self.authors_ui()

        self.stack.setCurrentIndex(0)

    # ================= THEMES =================
    def get_theme(self):
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

        title = QLabel("🐍 SNAKE GAME")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:32px;color:#2ecc71;font-weight:bold;")
        layout.addWidget(title)

        # SETTINGS
        self.multi_cb = QCheckBox("🎮 Multiplayer")
        self.magic_cb = QCheckBox("🍇 Magiczne owoce")
        self.wall_cb = QCheckBox("🌀 Wall Pass")
        self.magic_cb.setChecked(True)

        for c in [self.multi_cb, self.magic_cb, self.wall_cb]:
            c.setStyleSheet("color:white;padding:3px;")
            layout.addWidget(c)

        # SKIN
        self.skin_box = QComboBox()
        self.skin_box.addItems(["Neon", "Fire", "Ice"])
        self.skin_box.setStyleSheet("""
            background:#21262d;
            color:white;
            padding:6px;
            border-radius:6px;
        """)
        layout.addWidget(self.skin_box)

        # BUTTONS
        play = QPushButton("▶ GRAJ")
        info = QPushButton("📖 INSTRUKCJA")
        authors = QPushButton("👨‍💻 OD AUTOREK")

        play.clicked.connect(self.start_game)
        info.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        authors.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        for b in [play, info, authors]:
            b.setStyleSheet("""
                QPushButton {
                    background:#238636;
                    color:white;
                    padding:10px;
                    border-radius:10px;
                    font-weight:bold;
                }
                QPushButton:hover {
                    background:#2ea043;
                }
            """)
            layout.addWidget(b)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ================= GAME =================
    def game_ui(self):
        page = QWidget()
        layout = QVBoxLayout()

        self.hud = QLabel("SCORE: 0")
        self.hud.setStyleSheet("color:white;font-weight:bold;")

        self.canvas = GameCanvas(self)

        back = QPushButton("⬅ MENU")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        back.setStyleSheet("""
            background:#30363d;
            color:white;
            padding:8px;
            border-radius:8px;
        """)

        layout.addWidget(self.hud)
        layout.addWidget(self.canvas)
        layout.addWidget(back)

        page.setLayout(layout)
        self.stack.addWidget(page)

    # ================= INFO =================
    def info_ui(self):
        page = QWidget()
        layout = QVBoxLayout()

        text = QLabel("""
🐍 CEL: zbieraj owoce i rośnij
🎮 WASD / strzałki
🌀 Wall Pass = przechodzenie przez ściany
🍇 Magiczne owoce = bonus
🎨 3 skórki gracza
""")
        text.setStyleSheet("color:white;")

        back = QPushButton("⬅ POWRÓT")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

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
        title.setStyleSheet("""
            font-size:22px;
            color:#c77dff;
            font-weight:bold;
        """)

        text = QLabel("""
🎮 Snake PyQt Edition
💡 UI + Game Prototype
🚀 Projekt edukacyjny
🐍 Dziękujemy za uruchomienie gry!
""")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("color:white;")

        back = QPushButton("⬅ POWRÓT")
        back.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        back.setStyleSheet("""
            background:#238636;
            color:white;
            padding:10px;
            border-radius:10px;
            font-weight:bold;
        """)

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

        self.stack.setCurrentIndex(1)
        self.canvas.startGame()


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnakeApp()
    window.show()
    sys.exit(app.exec_())

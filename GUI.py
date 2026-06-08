import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QCheckBox,
    QStackedLayout
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

        klawisze_gracza = {
            Qt.Key_W: Direction.UP,
            Qt.Key_S: Direction.DOWN,
            Qt.Key_A: Direction.LEFT,
            Qt.Key_D: Direction.RIGHT
        }
        self.input_handler = InputHandler(klawisze_gracza)

    def startGame(self):
        self.difficulty = Difficulty(level=1, snake_speed=150, board_shape=BoardShape.ARENA)
        self.board = Board(20, 20, self.difficulty)
        self.snakes = [Snake(10, 10, color=self.parent.skin)]
        self.board.init_display(self)
        self.is_running = True
        self.timer.start(self.difficulty.getSpeed())
        self.setFocus()

    def keyPressEvent(self, event):
        self.input_handler.readInput(event.key())
        self.input_handler.sendDirection(self.snakes)

    def game_loop(self):
        if not self.snakes:
            return 
        waz = self.snakes[0]
        waz.move()
        self.checkCollision()
        self.render_game()
        self.parent.hud.setText(f"SCORE: {waz.score}")

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
        
        waz = self.snakes[0]
        for i, segment in enumerate(waz.body):
            if 0 <= segment.x < self.board.width and 0 <= segment.y < self.board.height:
                item = grid.itemAtPosition(segment.y, segment.x)
                if item and item.widget():
                    tile = item.widget()
                    if i == 0:
                        tile.setStyleSheet(f"background-color: {theme['snake']}; border: 2px solid #ffffff; border-radius: 4px;")
                    else:
                        tile.setStyleSheet(f"background-color: {theme['snake']}; border-radius: 2px;")

    def checkCollision(self):
        waz = self.snakes[0]
        glowa = waz.glowa
        
        if self.board.is_obstacle(glowa.x, glowa.y):
            if self.parent.wall_pass:
                pass 
            else:
                self.endGame()
                
        if waz.checkSelfHit():
            self.endGame()

    def endGame(self):
        self.timer.stop()
        self.parent.hud.setText(f"GAME OVER! SCORE: {self.snakes[0].score}")

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

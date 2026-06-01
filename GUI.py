import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QComboBox, QCheckBox,
    QStackedLayout
)
from PyQt5.QtCore import Qt


# ================= GAME CANVAS =================
class GameCanvas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setFixedSize(650, 420)

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

        self.canvas.update()
        self.stack.setCurrentIndex(1)


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SnakeApp()
    window.show()
    sys.exit(app.exec_())
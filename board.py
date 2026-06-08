from enum import Enum
from PyQt5.QtWidgets import QGridLayout, QLabel

class BoardShape(Enum):
    RECTANGLE = "RECTANGLE"
    MAZE = "MAZE"
    ARENA = "ARENA"

class Difficulty:
    def __init__(self, level: int, snake_speed: int, board_shape: BoardShape):
        self.level = level
        self.snake_speed = snake_speed
        self.board_shape = board_shape
    def getSpeed(self):
        return self.snake_speed
    def getShape(self):
        return self.board_shape
    
class Board:
    def __init__(self, width: int, height: int, difficulty: Difficulty):
        self.width = width
        self.height = height
        self.obstacles = []
        self.shape = difficulty.getShape()
        #dodanie ścian na początku
        self.generateWalls(self.shape)
    def drawBoard(self):
        szachownica = []
        for y in range(self.height):
            wiersz = []
            for x in range(self.width):
                #czy ściana
                if (x,y) in self.obstacles:
                    wiersz.append("WALL")
                # nie to szachownica
                elif (x + y) % 2 == 0:
                    wiersz.append("TILE_A")
                else:
                    wiersz.append("TILE_B")
            szachownica.append(wiersz)
        return szachownica
    def clearBoard(self):
        self.obstacles = []
    def generateWalls(self, shape: BoardShape):
        """x to kolumna (od 0 do self.width - 1)
           y to wiersz (od 0 do self.height - 1)"""
        self.obstacles = []
        if shape == BoardShape.RECTANGLE:
            self.obstacles = []
        elif shape == BoardShape.ARENA:
            for y in range(self.height):
                self.obstacles.append((0, y))
                self.obstacles.append((self.width - 1, y))
            for x in range(self.width):
                self.obstacles.append((x, 0))
                self.obstacles.append((x, self.height - 1))
        elif shape == BoardShape.MAZE:
            self.obstacles = []
            polowa_y = self.height // 2
            jedna_trzecia_y = self.height // 3

            # 1. Długie pionowe linie (3 kratki od brzegu)
            for y in range(2, polowa_y + 1):
                self.obstacles.append((2, y))                     
                self.obstacles.append((self.width - 3, y))         

            # 2. Krótsze pionowe linie (5 kratek od brzegu)
            for y in range(8, 12):
                self.obstacles.append((6, y))             
                self.obstacles.append((self.width - 7, y))
            # 3. Pozioma kreska
            for x in range(6, self.width - 6):
                self.obstacles.append((x, jedna_trzecia_y))
    def is_obstacle(self, x:int, y:int) -> bool:
        return (x,y) in self.obstacles
    def init_display(self, canvas):
        matrix = self.drawBoard()
        """Buduje graficzną siatkę planszy wewnątrz okna gry"""
        
        if canvas.layout() is None:
            grid = QGridLayout()
            grid.setSpacing(0)
            canvas.setLayout(grid)
        else:
            grid = canvas.layout()
            #Przed nową grą pozbywamy się starych ścian
            while grid.count():
                item = grid.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        theme = canvas.parent.get_theme()

        for y in range(self.height):
            for x in range(self.width):
                if self.is_obstacle(x, y):
                    style = "background-color: #1c2331; border: 1px solid #2b364a;"
                elif matrix[y][x] == "TILE_A":
                    style = f"background-color: {theme['bg']};"
                else:
                    # rgba(0,0,0,0.4) nałoży 40% przezroczystej czerni, 
                    # wtedy ten kafelek będzie automatycznie ciemniejszy od swoich sąsiadów niezależnie od motywu
                    #A przynajmniej taką mam nadzieję haha
                    style = f"background-color: {theme['bg']}; border: 1px solid rgba(0, 0, 0, 0.4);"
                tile = QLabel("")
                tile.setStyleSheet(style)
                grid.addWidget(tile, y, x)
        canvas.setLayout(grid)

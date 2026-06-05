from enum import Enum
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
        if shape == BoardShape.RECTANGLE:
            self.obstacles = []
        elif shape == BoardShape.ARENA:
            for y in range(self.height):
                self.obstacles.append((0, y))
                self.obstacles.append((self.width - 1, y))
        elif shape == BoardShape.MAZE:
            self.obstacles = [] #na razie
    def is_obstacle(self, x:int, y:int) -> bool:
        return (x,y) in self.obstacles

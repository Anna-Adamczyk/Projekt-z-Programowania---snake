from enum import Enum

from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget


class BoardShape(Enum):
    """Dostępne kształty planszy."""

    RECTANGLE = "RECTANGLE"
    MAZE = "MAZE"
    ARENA = "ARENA"


class Difficulty:
    """Przechowuje parametry wybranego poziomu trudności."""

    def __init__(
        self,
        level: int,
        snake_speed: int,
        board_shape: BoardShape,
    ) -> None:
        self.level = level
        self.snake_speed = snake_speed
        self.board_shape = board_shape

    def get_speed(self) -> int:
        """Zwraca prędkość poruszania się węża."""
        return self.snake_speed

    def get_shape(self) -> BoardShape:
        """Zwraca wybrany kształt planszy."""
        return self.board_shape


class Board:
    """Reprezentuje planszę gry wraz z przeszkodami."""

    def __init__(
        self,
        width: int,
        height: int,
        difficulty: Difficulty,
    ) -> None:
        self.width = width
        self.height = height
        self.obstacles: list[tuple[int, int]] = []
        self.shape = difficulty.get_shape()

        # Wygenerowanie ścian zgodnie z wybranym kształtem planszy.
        self.generate_walls(self.shape)

    def draw_board(self) -> list[list[str]]:
        """Tworzy i zwraca macierz reprezentującą aktualny stan planszy."""
        board = []

        for y in range(self.height):
            row = []

            for x in range(self.width):
                if (x, y) in self.obstacles:
                    row.append("WALL")
                elif (x + y) % 2 == 0:
                    row.append("TILE_A")
                else:
                    row.append("TILE_B")

            board.append(row)

        return board

    def clear_board(self) -> None:
        """Usuwa wszystkie przeszkody z planszy."""
        self.obstacles = []

    def generate_walls(self, shape: BoardShape) -> None:
        """Generuje przeszkody dla wybranego kształtu planszy.

        Współrzędna ``x`` oznacza kolumnę, a ``y`` oznacza wiersz.
        """
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
            half_height = self.height // 2
            third_height = self.height // 3

            # Długie pionowe ściany.
            for y in range(2, half_height + 1):
                self.obstacles.append((2, y))
                self.obstacles.append((self.width - 3, y))

            # Krótsze pionowe ściany.
            for y in range(11, 15):
                self.obstacles.append((6, y))
                self.obstacles.append((self.width - 7, y))

            # Pozioma ściana.
            for x in range(8, self.width - 6):
                self.obstacles.append((x, third_height))

    def is_obstacle(self, x: int, y: int) -> bool:
        """Sprawdza, czy wskazane pole zawiera przeszkodę."""
        return (x, y) in self.obstacles

    def init_display(self, canvas: QWidget) -> None:
        """Buduje graficzną reprezentację planszy na przekazanym widżecie."""
        matrix = self.draw_board()

        if canvas.layout() is None:
            grid = QGridLayout()
            grid.setSpacing(0)
            canvas.setLayout(grid)
        else:
            grid = canvas.layout()

            # Usunięcie elementów z poprzedniej planszy.
            while grid.count():
                item = grid.takeAt(0)

                if item.widget():
                    item.widget().deleteLater()

        theme = canvas.parent.get_theme()

        for y in range(self.height):
            for x in range(self.width):
                if self.is_obstacle(x, y):
                    style = (
                        "background-color: #1c2331;"
                        "border: 1px solid #2b364a;"
                    )
                elif matrix[y][x] == "TILE_A":
                    style = f"background-color: {theme['bg']};"
                else:
                    style = (
                        f"background-color: {theme['bg']};"
                        "border: 1px solid rgba(0, 0, 0, 0.4);"
                    )

                tile = QLabel("")
                tile.setStyleSheet(style)
                grid.addWidget(tile, y, x)

        if canvas.layout() is None:
            canvas.setLayout(grid)
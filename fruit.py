from random import randint
class Food:
    """Klasa reprezentująca standardowy owoc zwiększający wynik gracza."""
    def __init__(self, x: int = 0, y: int = 0, points: int = 1):
        self.x = x
        self.y = y
        self.points = points

    def getPosition(self) -> tuple[int, int]:
        """Zwraca aktualną pozycję owocu."""
        return (self.x, self.y)

    def spawn(self, board) -> None:
        """Losuje nową pozycję owocu na planszy."""
        while True:
            x = randint(1, board.width - 2)
            y = randint(1, board.height - 2)

            if not board.is_obstacle(x, y):
                self.x = x
                self.y = y
                break


class MagicFruit(Food):
    """Specjalny owoc aktywujący przyspieszenie węża."""
    def __init__(self, x=0, y=0):
        super().__init__(x, y, points=3)

        self.boostTime = 3
        self.speedBonus = 2

    def applyEffect(self, snake) -> None:
     """Aktywuje efekt przyspieszenia dla podanego węża."""
     snake.activateBoost(self.boostTime)
     snake.speed += self.speedBonus
from random import randint
class Food:
    def __init__(self, x=0, y=0, points=1):
        self.x = x
        self.y = y
        self.points = points

    def getPosition(self):
        return (self.x, self.y)

    def spawn(self, board):
        while True:
            x = randint(1, board.width - 2)
            y = randint(1, board.height - 2)

            if not board.is_obstacle(x, y):
                self.x = x
                self.y = y
                break


class MagicFruit(Food):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, points=3)

        self.boostTime = 3
        self.speedBonus = 2

    def applyEffect(self, snake):
     snake.activateBoost(self.boostTime)
     snake.speed += self.speedBonus
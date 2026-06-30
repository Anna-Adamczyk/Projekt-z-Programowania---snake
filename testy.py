import pytest

from board import Board, BoardShape, Difficulty
from fruit import Food, MagicFruit
from snake import Snake, Direction


#=====For Board=====

@pytest.mark.parametrize(
    "level, speed, shape",
    [
        (1, 150, BoardShape.RECTANGLE),
        (2, 100, BoardShape.ARENA),
        (3, 70, BoardShape.MAZE),
        (5, 50, BoardShape.RECTANGLE), 
    ],
)
def test_difficulty_get_speed_and_shape(level, speed, shape):
    difficulty = Difficulty(level, speed, shape)
    assert difficulty.get_speed() == speed
    assert difficulty.get_shape() == shape


@pytest.mark.parametrize(
    "shape",
    [BoardShape.ARENA, BoardShape.MAZE]
)
def test_clear_board_removes_all_obstacles(shape):
    difficulty = Difficulty(2, 100, shape)
    board = Board(20, 20, difficulty)

    assert len(board.obstacles) > 0  
    board.clear_board()
    assert board.obstacles == []     


@pytest.mark.parametrize(
    "shape, point, expected",
    [
        
        (BoardShape.ARENA, (0, 0), True),
        (BoardShape.ARENA, (19, 19), True),
        (BoardShape.ARENA, (10, 10), False),
        (BoardShape.ARENA, (0, 10), True),
        
        (BoardShape.RECTANGLE, (0, 0), False),
        (BoardShape.RECTANGLE, (5, 5), False),
    ],
)
def test_is_obstacle_scenarios(shape, point, expected):
    difficulty = Difficulty(1, 100, shape)
    board = Board(20, 20, difficulty)
    assert board.is_obstacle(*point) is expected


class MockBoard:
    width = 20
    height = 20

    def is_obstacle(self, x, y):
        
        return (x, y) == (5, 5)


#=====For Fruit=====

class MockSnake:
    def __init__(self):
        self.speed = 5
        self.boost_called = False
        self.boost_time = None

    def activateBoost(self, time):
        self.boost_called = True
        self.boost_time = time


def test_food_spawn_inside_board_and_respects_obstacles():
    board = MockBoard()
    food = Food()

    for _ in range(50):
        food.spawn(board)
        assert 1 <= food.x < board.width - 1
        assert 1 <= food.y < board.height - 1
        assert food.getPosition() != (5, 5) 


def test_magic_fruit_apply_effect():
    snake = MockSnake()
    fruit = MagicFruit()

    fruit.applyEffect(snake)

    assert snake.boost_called is True
    assert snake.boost_time == fruit.boostTime
    assert snake.speed == 7 


#=====For Snake=====

@pytest.mark.parametrize(
    "start_x, start_y, nowy_x, nowy_y, zjedzono",
    [
        (5, 5, 5, 4, False),  
        (5, 5, 6, 5, False),  
        (10, 10, 10, 11, True), 
        (10, 10, 9, 10, True),  
    ],
)
def test_snake_move_variations(start_x, start_y, nowy_x, nowy_y, zjedzono):
    snake = Snake(start_x, start_y)
    dlugosc_przed = len(snake.body)

    snake.move(nowy_x, nowy_y, zjedzono_owoc=zjedzono)

    assert snake.glowa.getPosition() == (nowy_x, nowy_y)
    if zjedzono:
        assert len(snake.body) == dlugosc_przed + 1
    else:
        assert len(snake.body) == dlugosc_przed


@pytest.mark.parametrize(
    "current, new, expected",
    [
        (Direction.UP, Direction.LEFT, Direction.LEFT),
        (Direction.UP, Direction.RIGHT, Direction.RIGHT),
        (Direction.LEFT, Direction.UP, Direction.UP),
        (Direction.LEFT, Direction.DOWN, Direction.DOWN),
        (Direction.UP, Direction.DOWN, Direction.UP),      
        (Direction.DOWN, Direction.UP, Direction.DOWN),      
        (Direction.LEFT, Direction.RIGHT, Direction.LEFT),
        (Direction.RIGHT, Direction.LEFT, Direction.RIGHT),
    ],
)
def test_change_direction_mechanics(current, new, expected):
    snake = Snake(5, 5)
    snake.direction = current

    snake.zmien_kierunek(new)

    assert snake.direction == expected


def test_snake_check_self_hit():
    snake = Snake(5, 5)
    
    snake.move(5, 4, zjedzono_owoc=True)
    snake.move(6, 4, zjedzono_owoc=True)
    
    assert snake.checkSelfHit() is False

    snake.move(6, 4, zjedzono_owoc=False)
    assert snake.checkSelfHit() is True


def test_snake_manual_boost():
    snake = Snake(5, 5)
    assert snake.manualBoost is False
    
    snake.ręczne_przyspieszenie()
    assert snake.manualBoost is True
    
    snake.resetuj_przyspieszenia()
    assert snake.manualBoost is False
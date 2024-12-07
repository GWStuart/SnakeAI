import random

class Game:
    SNAKE_SPAWN_POSITION = (20, 20)

    def __init__(self, LENGTH: int, HEIGHT: int, CELL_SIZE: int = 10):
        self.LENGTH = LENGTH
        self.HEIGHT = HEIGHT
        self.CELL_SIZE = 10

        self.snake = Snake(LENGTH, HEIGHT, CELL_SIZE, *Game.SNAKE_SPAWN_POSITION)

    """
    Updates the game and returns False if the game is over
    @returns False if the game is over and True otherwise
    """
    def update(self) -> bool:
        return self.snake.update()

    """
    Processes the given key press in the game.
    If the key press is invalid then nothing is done
    @param key the key press as a string
    @returns True if the key press was valid and False otherwise
    @ensures that snake.move is only called with a valid key
    """
    def sendKey(self, key: str) -> bool:
        if (key in ("l", "r", "u", "d")):
            self.snake.move(key)
            return True
        return False


    """
    Same as the sendKey function but removes safety checks making it marginally faster.
    This is good if you are sure that the provided key is valid
    @requires that the provided key is valid
    """
    def sendKeyFase(self, key: str):
        self.snake.move(key)

    def getSnakeBody(self) -> list[tuple[int]]:
        return self.snake.body

    def getApplePosition(self) -> tuple[int, int]:
        return self.snake.apple


class Snake:
    """
    Constructor for the snake
    @param x, y are the x and y initial coordinates of the snake
    """
    def __init__(self, LENGTH: int, HEIGHT: int, CELL_SIZE: int, x: int, y: int):
        self.LENGTH = LENGTH
        self.HEIGHT = HEIGHT
        self.XCELLS = LENGTH // CELL_SIZE
        self.YCELLS = HEIGHT // CELL_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.x = x
        self.y = y
        self.apple = self.getRandomCell()

        self.body = [(x, y)]

    def getRandomCell(self) -> tuple[int, int]:
        return random.randint(0, self.XCELLS) * self.CELL_SIZE, random.randint(0, self.YCELLS) * self.CELL_SIZE

    """
    Moves the snake in its direction of motion
    @param direciton the direction in which to move the snake
    """
    def move(self, direction: str):
        match direction:
            case "l":
                self.x -= self.CELL_SIZE
            case "r":
                self.x += self.CELL_SIZE 
            case "u":
                self.y -= self.CELL_SIZE
            case _:
                self.y += self.CELL_SIZE

        self.body.append((self.x, self.y))

    """
    Checks that the game is not over and checks if an apple has been eaten.
    This method should always be run after the snake as moved. I.e. after calling the move() method
    @returns False if the game is over and True otherwise
    """
    def update(self) -> bool:
        if self.isGameOver():
            return False

        if self.body[-1] == self.apple:  # check if the snake is on the apple
            self.apple = self.getRandomCell()
        else:
            self.body.pop(0)
        return True

    """
    checks if the game is over
    @returns True if the game is over and False otherwise
    """
    def isGameOver(self) -> bool:
        if self.x < 0 or self.x > self.LENGTH or self.y < 0 or self.y > self.HEIGHT:
            return True
        if self.body[-1] in self.body[:-1]:  # might be faster to compare body vs set() of body idk
            return True
        return False


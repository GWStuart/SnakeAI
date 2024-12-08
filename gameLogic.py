import random

class Game:
    SNAKE_SPAWN_POSITION = (2, 2)

    def __init__(self, XCELLS: int, YCELLS: int):
        self.XCELLS = XCELLS
        self.YCELLS = YCELLS

        self.snake = Snake(XCELLS, YCELLS, *Game.SNAKE_SPAWN_POSITION)

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
    @returns True if the move results in an eaten apple and False otherwise
    """
    def sendKeyFast(self, key: str):
        return self.snake.move(key)

    def getSnakeBody(self) -> list[tuple[int]]:
        return self.snake.body

    def getApplePosition(self) -> tuple[int, int]:
        return self.snake.apple

    def isGameOver(self) -> bool:
        return self.snake.isGameOver()

    def getScore(self) -> int:
        return self.snake.score

    def getSnakeHead(self) -> tuple[int, int]:
        return self.snake.body[-1]


class Snake:
    """
    Constructor for the snake
    @param x, y are the x and y initial coordinates of the snake
    """
    def __init__(self, XCELLS: int, YCELLS: int, x: int, y: int):
        self.XCELLS = XCELLS 
        self.YCELLS = YCELLS
        self.x = x
        self.y = y

        self.apple = self.getRandomCell()
        self.score = 0
        self.body = [(x, y)]

    def getRandomCell(self) -> tuple[int, int]:
        return random.randint(0, self.XCELLS - 1), random.randint(0, self.YCELLS - 1)

    """
    Moves the snake in its direction of motion
    @param direciton the direction in which to move the snake
    @returns True if an apple was eaten and false otherwise
    """
    def move(self, direction: str):
        match direction:
            case "l":
                self.x -= 1
            case "r":
                self.x += 1
            case "u":
                self.y -= 1
            case _:
                self.y += 1

        self.body.append((self.x, self.y))
        return self.update()

    """
    Checks that the game is not over and checks if an apple has been eaten.
    This method should always be run after the snake as moved. I.e. after calling the move() method
    @returns True if an apple was eaten and False otherwise
    """
    def update(self) -> bool:
        if self.body[-1] == self.apple:  # check if the snake is on the apple
            self.apple = self.getRandomCell()
            self.score += 1
            return True
        else:
            self.body.pop(0)
            return False

    """
    checks if the game is over
    @returns True if the game is over and False otherwise
    """
    def isGameOver(self) -> bool:
        if self.x < 0 or self.x > self.XCELLS - 1 or self.y < 0 or self.y > self.YCELLS - 1:
            return True
        if self.body[-1] in self.body[:-1]:  # might be faster to compare body vs set() of body idk
            return True
        return False


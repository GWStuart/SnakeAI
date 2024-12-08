import random

class Game:
    SNAKE_SPAWN_POSITION = (2, 2)

    def __init__(self, XCELLS: int, YCELLS: int):
        self.XCELLS = XCELLS
        self.YCELLS = YCELLS

        self.snake = Snake(XCELLS, YCELLS, *Game.SNAKE_SPAWN_POSITION)

    """
    Moves the snake in the given direction
    @requires that the provided direction is valid
    @param direction the direction in which to move the snake. If null then snake continues in current direction
    @returns True if the move results in an eaten apple and False otherwise
    """
    def moveSnake(self, direction: tuple[int, int]) -> bool:
        if not direction:
            direction = self.snake.direction
        else:
            match direction:
                case "l":
                    direction = (-1, 0)
                case "r":
                    direction = (1, 0)
                case "u":
                    direction = (0, -1)
                case "d":
                    direction = (0, 1)
        return self.snake.move(direction)

    """
    Moves the snake's head to the specified new position.
    This is essentially a more direct way of motion than the moveSnake
    @requires that the provided head position is valid.
    @param coordinates of the new head position
    @returns True if the move results in an eaten apple and False otherwise
    """
    def moveSnakeDirect(self, newHead: tuple[int, int]) -> bool:
        return self.snake.moveDirect(newHead)

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
    Moves the snakes in the specified direction
    @param the location to move the head to
    @requires that the new head position is valid
    @returns True if an apple was eaten and false otherwise
    """
    def move(self, direction: tuple[int, int]) -> bool:
        self.x += direction[0]
        self.y += direction[1]
        self.body.append((self.x, self.y))
        return self.update()

    """
    Moves the snakes head to the specified position
    @param the location to move the head to
    @requires that the new head position is valid
    @returns True if an apple was eaten and false otherwise
    """
    def moveDirect(self, newHead: tuple[int, int]) -> bool:
        self.x, self.y = newHead
        self.body.append(newHead)
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


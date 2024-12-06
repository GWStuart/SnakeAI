
class Game:
    SNAKE_SPAWN_POSITION = (20, 20)

    def __init__(self, LENGTH: int, HEIGHT: int):
        self.LENGTH = LENGTH
        self.HEIGHT = HEIGHT

        self.snake = Snake(LENGTH, HEIGHT, *Game.SNAKE_SPAWN_POSITION)

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


class Snake:
    CELL_SIZE = 10

    """
    Constructor for the snake
    @param x, y are the x and y initial coordinates of the snake
    """
    def __init__(self, LENGTH: int, HEIGHT: int, x: int, y: int):
        self.LENGTH = LENGTH
        self.HEIGHT = HEIGHT
        self.x = x
        self.y = y

        self.body = [(x, y)]

    """
    Moves the snake in its direction of motion
    @param direciton the direction in which to move the snake
    """
    def move(self, direction: str):
        match direction:
            case "l":
                self.x -= Snake.CELL_SIZE
            case "r":
                self.x += Snake.CELL_SIZE 
            case "u":
                self.y -= Snake.CELL_SIZE
            case _:
                self.y += Snake.CELL_SIZE

        self.body.append((self.x, self.y))

        self.body.pop(0)  # remove the last element

